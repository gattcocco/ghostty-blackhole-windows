"""Manual test: python bh-drive.py 0.5 | sweep --seconds 35 | off."""
import argparse
import importlib.util
import math
from pathlib import Path
import time

spec = importlib.util.spec_from_file_location("bridge", Path(__file__).with_name("claude-token.py"))
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("level", help="0..1, sweep, or off")
    parser.add_argument("--seconds", type=float, default=35)
    parser.add_argument("--reverse", action="store_true")
    args = parser.parse_args()
    if not math.isfinite(args.seconds) or args.seconds <= 0:
        parser.error("--seconds must be finite and positive")
    def send(level):
        if bridge.apply(level) is False:
            parser.exit(1, "No writable console. Run inside the experimental Ghostty window.\n")
    if args.level == "sweep":
        start = time.monotonic()
        try:
            for step in range(101):
                time.sleep(max(0, start + args.seconds * step / 100 - time.monotonic()))
                send(1 - step / 100 if args.reverse else step / 100)
        except KeyboardInterrupt:
            bridge.apply(-1)
            return
    else:
        try:
            level = -1 if args.level == "off" else float(args.level)
        except ValueError:
            parser.error("Use 0..1, sweep, or off")
        if args.level != "off" and (not math.isfinite(level) or not 0 <= level <= 1):
            parser.error("Level must be between 0 and 1")
        send(level)
    time.sleep(1.6)


if __name__ == "__main__":
    main()
