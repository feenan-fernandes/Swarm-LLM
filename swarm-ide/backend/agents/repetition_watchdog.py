"""
repetition_watchdog.py — Anti-Degeneration & Repetition Watchdog
Protects local LLM inference against degenerative repetition loops,
echo cycles, and autoregressive stalling.
"""

from typing import Tuple, Dict, Any

# Standard production Ollama generation options to inhibit token echo loops
DEFAULT_OLLAMA_OPTIONS: Dict[str, Any] = {
    "temperature": 0.2,
    "repeat_penalty": 1.18,
    "repeat_last_n": 128,
    "top_k": 40,
    "top_p": 0.90,
}


def build_ollama_options(temperature: float = 0.2, extra_options: dict = None) -> dict:
    """Builds a complete Ollama options dict including anti-repetition hyperparameters."""
    opts = dict(DEFAULT_OLLAMA_OPTIONS)
    opts["temperature"] = temperature
    if extra_options:
        opts.update(extra_options)
    return opts


class RepetitionStreamFilter:
    """
    Streaming watchdog that monitors incoming tokens from Ollama.
    Detects when a model gets stuck repeating the same sentence, paragraph,
    or substring cycle 3+ times, signaling the generator to halt gracefully.
    """
    def __init__(self, min_cycle_len: int = 20, max_cycle_len: int = 350, max_repeats: int = 3, check_window: int = 1500):
        self.buffer = ""
        self.min_cycle_len = min_cycle_len
        self.max_cycle_len = max_cycle_len
        self.max_repeats = max_repeats
        self.check_window = check_window
        self.loop_detected = False

    def push(self, chunk: str) -> bool:
        """
        Pushes a new chunk into the buffer.
        Returns True if output is healthy, False if a degenerative loop is detected.
        """
        if self.loop_detected:
            return False

        self.buffer += chunk
        window = self.buffer[-self.check_window:]
        w_len = len(window)

        # 1. Consecutive identical line check
        lines = [l.strip() for l in window.split('\n') if len(l.strip()) > 18]
        if len(lines) >= self.max_repeats:
            last = lines[-1]
            if lines[-self.max_repeats:] == [last] * self.max_repeats:
                self.loop_detected = True
                return False

        # 2. Cyclic suffix matching
        max_possible_c = min(self.max_cycle_len, w_len // self.max_repeats)
        for c_len in range(self.min_cycle_len, max_possible_c + 1):
            pattern = window[-c_len:]
            repeats = 1
            pos = w_len - c_len
            while pos >= c_len and window[pos - c_len:pos] == pattern:
                repeats += 1
                pos -= c_len
                if repeats >= self.max_repeats:
                    self.loop_detected = True
                    return False

        return True


def sanitize_repetition(text: str, max_consecutive_lines: int = 1) -> str:
    """
    Sanitizes non-streaming responses by stripping runaway repetitive blocks,
    consecutive duplicate paragraphs, and tail repetition loops.
    """
    if not text:
        return text

    # 1. Deduplicate consecutive identical lines/paragraphs (> 20 chars)
    lines = text.split('\n')
    cleaned_lines = []
    repeat_count = 0
    last_line = None

    for line in lines:
        stripped = line.strip()
        if len(stripped) > 20 and stripped == last_line:
            repeat_count += 1
            if repeat_count >= max_consecutive_lines:
                continue
        else:
            repeat_count = 0
            last_line = stripped if len(stripped) > 20 else None
        cleaned_lines.append(line)

    text = '\n'.join(cleaned_lines)

    # 2. Check and prune cyclic suffix loops
    for c_len in range(25, min(350, len(text) // 3) + 1):
        pattern = text[-c_len:]
        repeats = 1
        pos = len(text) - c_len
        while pos >= c_len and text[pos - c_len:pos] == pattern:
            repeats += 1
            pos -= c_len
        if repeats >= 3:
            return text[:pos + c_len].rstrip()

    return text
