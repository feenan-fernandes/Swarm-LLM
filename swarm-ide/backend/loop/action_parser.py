"""
action_parser.py — Updated with <patch_file> tag (Phase 6)
All 11 action tags from Section 5 + patch_file.
"""
import re
import json


def _extract(text, tag, flags=re.DOTALL | re.IGNORECASE):
    m = re.search(rf'<{tag}>(.*?)</{tag}>', text, flags)
    return m.group(1).strip() if m else None


def _extract_attr(text, tag, attr):
    m = re.search(rf'<{tag}[^>]*\b{attr}=["\']([^"\']*)["\']', text, re.IGNORECASE)
    return m.group(1).strip() if m else None


def extract_thought(xml_text):
    return _extract(xml_text, "think") or ""


def _normalize_tool_args(action_type, args):
    if not isinstance(args, dict):
        return args

    # Handle execute_bash
    if action_type == "execute_bash":
        if "cmd" in args and "command" not in args:
            args["command"] = args.pop("cmd")
    # Handle write_file
    elif action_type == "write_file":
        if "filename" in args and "path" not in args:
            args["path"] = args.pop("filename")
        elif "file" in args and "path" not in args:
            args["path"] = args.pop("file")
    # Handle run_test
    elif action_type == "run_test":
        if "cmd" in args and "command" not in args:
            args["command"] = args.pop("cmd")
    # Handle ask_user
    elif action_type == "ask_user":
        if "q" in args and "question" not in args:
            args["question"] = args.pop("q")
    # Handle spawn_worker
    elif action_type == "spawn_worker":
        if "workers" not in args:
            if "tasks" in args:
                args["workers"] = args["tasks"]
            elif "task" in args:
                args["workers"] = [{"task": args["task"], "skill": args.get("skill", ""), "role": args.get("role", "Specialized Sub-Agent")}]
    # Handle update_memory
    elif action_type == "update_memory":
        if "target" not in args:
            args["target"] = "project"
    # Handle create_skill
    elif action_type == "create_skill":
        if "slug" not in args and "name" in args:
            args["slug"] = args["name"].lower().replace(" ", "-")

    return args


def _parse_nous_tool_call(xml_text):
    """
    Parses Nous Research Hermes native <tool_call> format containing JSON or function tags:
    <tool_call>
    {"name": "write_file", "arguments": {"path": "main.py", "content": "..."}}
    </tool_call>
    """
    m = re.search(r'<tool_call>(.*?)</tool_call>', xml_text, re.DOTALL | re.IGNORECASE)
    if not m:
        return None
    raw = m.group(1).strip()
    if raw.startswith("```"):
        raw = re.sub(r'^```[a-zA-Z]*\n', '', raw)
        raw = re.sub(r'\n```$', '', raw).strip()

    try:
        data = json.loads(raw)
        if isinstance(data, dict):
            name = data.get("name") or data.get("tool") or data.get("action") or ""
            args = data.get("arguments") or data.get("parameters") or data.get("args") or {}
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except Exception:
                    args = {"input": args}
            if name:
                args = _normalize_tool_args(name, args)
                return {"type": name, "args": args}
    except Exception:
        pass

    # Fallback: <function=...><parameter=...>...</function> style
    fn_m = re.search(r'<function=([^>]+)>(.*?)</function>', raw, re.DOTALL | re.IGNORECASE)
    if fn_m:
        fn_name = fn_m.group(1).strip()
        body = fn_m.group(2)
        params = {}
        for p_m in re.finditer(r'<parameter=([^>]+)>(.*?)</parameter>', body, re.DOTALL | re.IGNORECASE):
            params[p_m.group(1).strip()] = p_m.group(2).strip()
        params = _normalize_tool_args(fn_name, params)
        return {"type": fn_name, "args": params}

    return None


def parse_action(xml_text):
    """
    Returns {"type": str, "args": dict} for the first valid action tag found, or None.
    Handles Nous <tool_call>, all Section 5 tags, patch_file, update_memory, and create_skill.
    """

    # 0. Hermes Native <tool_call> Check
    nous_call = _parse_nous_tool_call(xml_text)
    if nous_call:
        return nous_call

    if "<plan>" in xml_text:
        return {"type": "plan", "args": {
            "goal": _extract(xml_text, "goal") or "",
            "steps": _extract(xml_text, "steps") or "",
            "acceptance_criteria": _extract(xml_text, "acceptance_criteria") or "",
        }}

    if "<search_github_skills>" in xml_text:
        return {"type": "search_github_skills", "args": {
            "query": _extract(xml_text, "query") or "",
            "topics": _extract(xml_text, "topics") or "",
            "min_stars": int(_extract(xml_text, "min_stars") or 0),
        }}

    if "<evaluate_skill>" in xml_text:
        return {"type": "evaluate_skill", "args": {
            "repo_url": _extract(xml_text, "repo_url") or "",
        }}

    if "<install_skill>" in xml_text:
        return {"type": "install_skill", "args": {
            "repo_url": _extract(xml_text, "repo_url") or "",
            "target_path": _extract(xml_text, "target_path") or "",
        }}

    if "<select_skill>" in xml_text:
        return {"type": "select_skill", "args": {
            "skill_name": _extract(xml_text, "skill_name") or "",
            "reason": _extract(xml_text, "reason") or "",
        }}


    if "<replace_block>" in xml_text:
        return {"type": "replace_block", "args": {
            "path": _extract(xml_text, "path") or "",
            "search": _extract(xml_text, "search") or "",
            "replace": _extract(xml_text, "replace") or "",
        }}
    if "<patch_file>" in xml_text:
        return {"type": "patch_file", "args": {
            "path": _extract(xml_text, "path") or "",
            "diff": _extract(xml_text, "diff") or "",
        }}

    if "<update_memory" in xml_text:
        target = _extract_attr(xml_text, "update_memory", "target") or _extract(xml_text, "target") or "project"
        content = _extract(xml_text, "content") or ""
        if not content:
            m = re.search(r'<update_memory[^>]*>(.*?)</update_memory>', xml_text, re.DOTALL)
            content = m.group(1).strip() if m else ""
        return {"type": "update_memory", "args": {
            "target": target,
            "content": content
        }}

    if "<create_skill" in xml_text:
        name = _extract(xml_text, "name") or _extract_attr(xml_text, "create_skill", "name") or ""
        slug = _extract(xml_text, "slug") or _extract_attr(xml_text, "create_skill", "slug") or name.lower().replace(" ", "-")
        description = _extract(xml_text, "description") or _extract_attr(xml_text, "create_skill", "description") or ""
        category = _extract(xml_text, "category") or _extract_attr(xml_text, "create_skill", "category") or "tool"
        instructions = _extract(xml_text, "instructions") or _extract(xml_text, "content") or ""
        code = _extract(xml_text, "code") or _extract_attr(xml_text, "create_skill", "code") or ""
        if not code and not instructions:
            m = re.search(r'<create_skill[^>]*>(.*?)</create_skill>', xml_text, re.DOTALL)
            if m and not "<name>" in m.group(1):
                code = m.group(1).strip()
        return {"type": "create_skill", "args": {
            "name": name,
            "slug": slug,
            "description": description,
            "category": category,
            "instructions": instructions,
            "code": code,
        }}

    if "<use_skill" in xml_text:
        name = _extract(xml_text, "name") or _extract_attr(xml_text, "use_skill", "name") or ""
        args = _extract(xml_text, "args") or _extract_attr(xml_text, "use_skill", "args") or ""
        if not args:
            m = re.search(r'<use_skill[^>]*>(.*?)</use_skill>', xml_text, re.DOTALL)
            if m and not "<name>" in m.group(1):
                args = m.group(1).strip()
        return {"type": "use_skill", "args": {
            "name": name,
            "args": args,
        }}

    if "<create_ppt" in xml_text:
        path = _extract(xml_text, "path") or _extract_attr(xml_text, "create_ppt", "path") or "presentation.pptx"
        content = _extract(xml_text, "content") or ""
        return {"type": "create_ppt", "args": {"path": path, "content": content}}

    if "<write_file" in xml_text:
        path = _extract(xml_text, "path") or _extract_attr(xml_text, "write_file", "path") or ""
        content = _extract(xml_text, "content") or _extract_attr(xml_text, "write_file", "content") or ""
        if not content:
            # Maybe the content is just inside the write_file tags?
            m = re.search(r'<write_file[^>]*>(.*?)</write_file>', xml_text, re.DOTALL)
            if m and not "<path>" in m.group(1):
                content = m.group(1).strip()
        return {"type": "write_file", "args": {
            "path": path,
            "content": content,
        }}

    if "<execute_bash" in xml_text:
        cmd = _extract(xml_text, "command") or _extract(xml_text, "cmd") or _extract_attr(xml_text, "execute_bash", "command") or ""
        if not cmd:
            m = re.search(r'<execute_bash[^>]*>(.*?)</execute_bash>', xml_text, re.DOTALL)
            if m: cmd = m.group(1).strip()
        return {"type": "execute_bash", "args": {"command": cmd}}

    if "<run_test>" in xml_text:
        cmd = _extract(xml_text, "command") or _extract(xml_text, "cmd") or ""
        return {"type": "run_test", "args": {
            "command": cmd,
            "expect": _extract(xml_text, "expect") or "",
        }}

    if "<self_heal>" in xml_text:
        return {"type": "self_heal", "args": {
            "error_summary": _extract(xml_text, "error_summary") or "",
            "hypothesis": _extract(xml_text, "hypothesis") or "",
        }}

    if "<finish" in xml_text:
        status = (
            _extract_attr(xml_text, "finish", "status")
            or _extract(xml_text, "status")
            or "success"
        )
        summary = _extract(xml_text, "summary") or ""
        if not summary:
            m = re.search(r'<finish[^>]*>(.*?)</finish>', xml_text, re.DOTALL)
            summary = m.group(1).strip() if m else ""
        return {"type": "finish", "args": {"status": status, "summary": summary}}


    if "<search_web>" in xml_text:
        return {"type": "search_web", "args": {
            "query": _extract(xml_text, "query") or ""
        }}

    if "<mcp_call" in xml_text:
        server = _extract(xml_text, "server") or _extract_attr(xml_text, "mcp_call", "server") or ""
        tool = _extract(xml_text, "tool") or _extract_attr(xml_text, "mcp_call", "tool") or ""
        raw_args = _extract(xml_text, "arguments") or _extract(xml_text, "args") or "{}"
        try:
            parsed_args = json.loads(raw_args) if isinstance(raw_args, str) and raw_args.strip().startswith("{") else {"input": raw_args}
        except Exception:
            parsed_args = {"input": raw_args}
        return {"type": "mcp_call", "args": {
            "server": server,
            "tool": tool,
            "arguments": parsed_args
        }}

    if "<render_hyperframes_video" in xml_text:
        composition_html = _extract(xml_text, "composition_html") or _extract_attr(xml_text, "render_hyperframes_video", "composition_html") or ""
        output_filename = _extract(xml_text, "output_filename") or _extract_attr(xml_text, "render_hyperframes_video", "output_filename") or ""
        if not composition_html:
            m = re.search(r'<composition_html[^>]*>(.*?)</composition_html>', xml_text, re.DOTALL)
            if m: composition_html = m.group(1).strip()
        return {"type": "render_hyperframes_video", "args": {
            "composition_html": composition_html,
            "output_filename": output_filename,
        }}

    if "<ask_user>" in xml_text:
        return {"type": "ask_user", "args": {
            "question": _extract(xml_text, "question") or ""
        }}

    if "<search_rag>" in xml_text:
        return {"type": "search_rag", "args": {
            "index_name": _extract(xml_text, "index_name") or "",
            "query": _extract(xml_text, "query") or ""
        }}

    # Check for <spawn_worker> before falling back to generic markdown code blocks
    worker_blocks = re.findall(r'<spawn_worker>(.*?)</spawn_worker>', xml_text, re.DOTALL | re.IGNORECASE)
    if worker_blocks:
        workers = []
        for block in worker_blocks:
            task = _extract(block, "task")
            if not task:
                inner = re.sub(r'<[^>]+>.*?</[^>]+>', '', block).strip()
                task = inner if inner else block.strip()
            skill = _extract(block, "skill") or ""
            role = _extract(block, "role") or "Specialized Worker"
            if task:
                workers.append({"task": task, "skill": skill, "role": role})
        if workers:
            return {"type": "spawn_worker", "args": {"workers": workers, "tasks": workers}}

    m_bash = re.search(r'```bash\s*\n?(.*?)\n?```', xml_text, re.DOTALL | re.IGNORECASE)
    if m_bash:
        return {"type": "execute_bash", "args": {"command": m_bash.group(1).strip()}}

    m_python = re.search(r'```python\s*\n?(.*?)\n?```', xml_text, re.DOTALL | re.IGNORECASE)
    if m_python:
        return {"type": "write_file", "args": {"path": "scratch.py", "content": m_python.group(1).strip()}}

    m_html = re.search(r'```(?:html|wireframe|javascript|css|xml|mermaid)\s*\n?(.*?)\n?```', xml_text, re.DOTALL | re.IGNORECASE)
    if m_html:
        return {'type': 'write_file', 'args': {'path': 'index.html', 'content': m_html.group(1).strip()}}

    stripped_text = xml_text.strip()
    if len(stripped_text) > 20:
        return {"type": "finish", "args": {"summary": stripped_text}}

    return None
