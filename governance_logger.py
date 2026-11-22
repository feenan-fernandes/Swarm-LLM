import sqlite3
import uuid
import re
import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'governance.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            model TEXT,
            is_uncensored BOOLEAN,
            start_time TEXT,
            end_time TEXT,
            status TEXT,
            total_prompt_tokens INTEGER DEFAULT 0,
            total_completion_tokens INTEGER DEFAULT 0,
            total_latency_sec REAL DEFAULT 0.0
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS actions (
            id TEXT PRIMARY KEY,
            session_id TEXT,
            iteration INTEGER,
            thought TEXT,
            action_type TEXT,
            content TEXT,
            result TEXT,
            is_violation BOOLEAN,
            FOREIGN KEY(session_id) REFERENCES sessions(id)
        )
    ''')
    conn.commit()
    conn.close()

def start_session(model, is_uncensored):
    session_id = uuid.uuid4().hex
    start_time = datetime.datetime.utcnow().isoformat()
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO sessions (id, model, is_uncensored, start_time, status) VALUES (?, ?, ?, ?, ?)',
              (session_id, model, is_uncensored, start_time, 'RUNNING'))
    conn.commit()
    conn.close()
    return session_id

def evaluate_safety(action_type, content):
    """
    Evaluates Trajectory Assurance constraints.
    Returns True if a sandbox violation is detected.
    """
    if action_type != 'execute_bash':
        return False
        
    unsafe_patterns = [
        r'rm\s+-rf\s+/',           # Catastrophic delete
        r'\.env',                  # Accessing environment variables
        r'cat\s+/etc/passwd',      # Sensitive system files
        r'nmap',                   # Network scanning
        r'wget\s+http',            # Blind payload downloads (context dependent, but good to flag)
        r'curl\s+.*\|\s*bash'      # Execution of remote scripts
    ]
    
    for pattern in unsafe_patterns:
        if re.search(pattern, str(content), re.IGNORECASE):
            return True
            
    return False

def log_action(session_id, iteration, thought, action_type, content, result, metrics):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT is_uncensored FROM sessions WHERE id = ?', (session_id,))
    row = c.fetchone()
    if row and row[0]:
        conn.close()
        return False  # Bypass logging and safety checks for Heretic mode
        
    action_id = uuid.uuid4().hex
    is_violation = evaluate_safety(action_type, content)
    
    # Update Session Aggregates
    prompt_tokens = metrics.get('prompt_tokens', 0)
    completion_tokens = metrics.get('completion_tokens', 0)
    eval_duration_sec = metrics.get('eval_duration', 0) / 1e9
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO actions (id, session_id, iteration, thought, action_type, content, result, is_violation)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (action_id, session_id, iteration, thought, action_type, str(content), str(result), is_violation))
    
    # Aggregate metrics to session
    c.execute('''
        UPDATE sessions 
        SET total_prompt_tokens = total_prompt_tokens + ?,
            total_completion_tokens = total_completion_tokens + ?,
            total_latency_sec = total_latency_sec + ?
        WHERE id = ?
    ''', (prompt_tokens, completion_tokens, eval_duration_sec, session_id))
    
    conn.commit()
    conn.close()
    return is_violation

def end_session(session_id, status):
    end_time = datetime.datetime.utcnow().isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE sessions SET status = ?, end_time = ? WHERE id = ?', (status, end_time, session_id))
    conn.commit()
    conn.close()

def get_governance_metrics():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    try:
        # Total Sessions
        c.execute('SELECT COUNT(*) as cnt FROM sessions')
        total_sessions = c.fetchone()['cnt']
        
        # Uncensored (Heretic) Sessions
        c.execute('SELECT COUNT(*) as cnt FROM sessions WHERE is_uncensored = 1')
        uncensored_sessions = c.fetchone()['cnt']
        
        # Total Logged Actions
        c.execute('SELECT COUNT(*) as cnt FROM actions')
        total_actions = c.fetchone()['cnt']
        
        # Thrashing Sessions (status FAILED/THRASHING)
        c.execute("SELECT COUNT(*) as cnt FROM sessions WHERE status = 'THRASHING' OR status = 'FAILED'")
        thrashing_sessions = c.fetchone()['cnt']
        
        # Sandbox Trajectory Violations
        c.execute('SELECT COUNT(*) as cnt FROM actions WHERE is_violation = 1')
        total_violations = c.fetchone()['cnt']
        
        # FinOps (Total Tokens & Latency)
        c.execute('SELECT SUM(total_prompt_tokens) as p, SUM(total_completion_tokens) as c, SUM(total_latency_sec) as t FROM sessions')
        row = c.fetchone()
        total_prompt = row['p'] or 0
        total_completion = row['c'] or 0
        total_time = row['t'] or 0.0
        
        # Recent violations (last 5)
        c.execute('SELECT action_type, content, result FROM actions WHERE is_violation = 1 ORDER BY rowid DESC LIMIT 5')
        recent_violations = [dict(r) for r in c.fetchall()]
        
        # Recent Actions (last 10)
        c.execute('SELECT session_id, iteration, action_type, content, result, is_violation FROM actions ORDER BY rowid DESC LIMIT 10')
        recent_actions = []
        for r in c.fetchall():
            d = dict(r)
            content_str = str(d.get('content') or '')
            result_str = str(d.get('result') or '')
            d['content_snippet'] = (content_str[:120] + '...') if len(content_str) > 120 else content_str
            d['result_snippet'] = (result_str[:120] + '...') if len(result_str) > 120 else result_str
            recent_actions.append(d)
            
        # Model usage distribution
        c.execute('SELECT model, COUNT(*) as cnt FROM sessions GROUP BY model ORDER BY cnt DESC LIMIT 5')
        model_dist = [dict(r) for r in c.fetchall()]
        
        return {
            "total_sessions": total_sessions,
            "uncensored_sessions": uncensored_sessions,
            "total_actions": total_actions,
            "thrashing_sessions": thrashing_sessions,
            "total_violations": total_violations,
            "total_tokens": total_prompt + total_completion,
            "total_compute_time": round(total_time, 2),
            "thrashing_rate": round((thrashing_sessions / total_sessions * 100) if total_sessions > 0 else 0, 1),
            "recent_violations": recent_violations,
            "recent_actions": recent_actions,
            "model_dist": model_dist
        }
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
    print("Governance Database Initialized.")
