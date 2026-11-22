import sys
import os
import unittest
import importlib

# Add swarm-ide to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'swarm-ide')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import governance_logger
from backend.agents.repetition_watchdog import (
    build_ollama_options,
    RepetitionStreamFilter,
    sanitize_repetition,
    DEFAULT_OLLAMA_OPTIONS
)
from backend.agents.orchestrator import call_orchestrator, stream_orchestrator


class TestGovernanceAndAntiRepetition(unittest.TestCase):

    def test_governance_metrics(self):
        metrics = governance_logger.get_governance_metrics()
        self.assertIn("total_sessions", metrics)
        self.assertIn("uncensored_sessions", metrics)
        self.assertIn("total_actions", metrics)
        self.assertIn("total_tokens", metrics)
        self.assertIn("total_compute_time", metrics)
        self.assertIn("thrashing_rate", metrics)
        self.assertIn("recent_actions", metrics)
        self.assertIn("recent_violations", metrics)
        self.assertIn("model_dist", metrics)
        self.assertGreaterEqual(metrics["total_sessions"], 0)
        self.assertGreaterEqual(metrics["uncensored_sessions"], 0)
        self.assertIsInstance(metrics["recent_actions"], list)

    def test_ollama_anti_repetition_options(self):
        opts = build_ollama_options(temperature=0.25)
        self.assertEqual(opts["temperature"], 0.25)
        self.assertEqual(opts["repeat_penalty"], 1.18)
        self.assertEqual(opts["repeat_last_n"], 128)
        self.assertEqual(opts["top_p"], 0.90)

    def test_streaming_repetition_watchdog_loop_detection(self):
        rf = RepetitionStreamFilter(min_cycle_len=20, max_repeats=3)
        loop_segment = "Add a Stand: Cut out a piece of cardboard or foam board to serve as the stand.\n"

        # Healthy tokens
        self.assertTrue(rf.push("Step 1: Gather cardboard and scissors.\n"))
        self.assertTrue(rf.push("Step 2: Paint the backdrop blue.\n"))

        # Repetition cycle begins
        self.assertTrue(rf.push(loop_segment))
        self.assertTrue(rf.push(loop_segment))
        # 3rd repeat triggers watchdog
        self.assertFalse(rf.push(loop_segment))
        self.assertTrue(rf.loop_detected)
        # Any subsequent chunk is rejected
        self.assertFalse(rf.push(loop_segment))

    def test_sanitize_repetition_multiline(self):
        sample = (
            "Add Details: Use construction paper.\n"
            "Add Color: Use paints.\n"
            "Add a Base: Cut out a piece of cardboard.\n"
            "Add a Stand: Cut out a piece of cardboard or foam board to serve as the stand for your diorama.\n"
            "Add a Stand: Cut out a piece of cardboard or foam board to serve as the stand for your diorama.\n"
            "Add a Stand: Cut out a piece of cardboard or foam board to serve as the stand for your diorama.\n"
            "Add a Stand: Cut out a piece of cardboard or foam board to serve as the stand for your diorama.\n"
        )
        cleaned = sanitize_repetition(sample)
        self.assertEqual(cleaned.count("Add a Stand"), 1)
        self.assertIn("Add Details: Use construction paper.", cleaned)
        self.assertIn("Add Color: Use paints.", cleaned)
        self.assertIn("Add a Base: Cut out a piece of cardboard.", cleaned)

    def test_sanitize_repetition_cyclic_suffix(self):
        phrase = "This is a repeating sentence that loops endlessly over and over again without stop. "
        text = "Valid prefix. " + (phrase * 8)
        cleaned = sanitize_repetition(text)
        self.assertLess(cleaned.count(phrase.strip()), 4)
        self.assertTrue(cleaned.startswith("Valid prefix."))

    def test_flask_governance_route(self):
        builder_mod = importlib.import_module("6_builder_app")
        app = builder_mod.app
        client = app.test_client()
        res = client.get('/api/governance')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn('total_sessions', data)
        self.assertIn('uncensored_sessions', data)
        self.assertIn('recent_actions', data)


if __name__ == '__main__':
    unittest.main()
