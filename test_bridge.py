import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("bridge", ROOT / "claude-token.py")
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)


class BridgeTests(unittest.TestCase):
    def test_all_encoded_levels_round_trip(self):
        for value in range(251):
            with patch.object(bridge, "emit") as emit:
                bridge.apply(value / 250)
            seq = emit.call_args.args[0]
            rgb = bytes.fromhex(seq.decode("ascii")[6:-1])
            r, g, b = rgb
            self.assertEqual((r >> 4, g >> 4, b >> 4), (15, 11, 0))
            self.assertEqual(r & 15, (g & 15) ^ (b & 15) ^ 5)
            self.assertEqual(((g & 15) << 4) | (b & 15), value)

    def test_end_resets_and_transport_failure_propagates(self):
        with patch.object(bridge, "emit", return_value=False) as emit:
            self.assertFalse(bridge.apply(-1))
            emit.assert_called_once_with(b"\x1b]112\x07")
            self.assertFalse(bridge.apply(0.5))

    def test_context_percentage(self):
        self.assertAlmostEqual(bridge.context_fill({"context_window": {"used_percentage": 61}}), .61)
        self.assertEqual(bridge.context_fill({}), 0)
        self.assertEqual(bridge.context_fill({"context_window": {"used_percentage": 120}}), 1)

    def test_statusline_with_redirected_output(self):
        result = subprocess.run([sys.executable, str(ROOT / "claude-token.py")],
            input=json.dumps({"context_window": {"used_percentage": 61}}),
            capture_output=True, text=True, encoding="utf-8", timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("61%", result.stdout)
        self.assertNotIn("\x1b]12;", result.stdout)


if __name__ == "__main__":
    unittest.main()
