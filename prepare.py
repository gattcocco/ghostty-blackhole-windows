"""Generate local configs; never edits the user's Ghostty or Claude settings."""
import json
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parent
shader = (root / "blackhole.glsl").read_text(encoding="utf-8")
preview, count = re.subn(r"(#define\s+TOKEN_LEVEL\s+)[^\s/]+", r"\g<1>0.5", shader, count=1)
if count != 1:
    raise SystemExit("Cannot locate TOKEN_LEVEL; upstream shader changed")
(root / "blackhole-preview.glsl").write_text(preview, encoding="utf-8")
for name, file in [("preview", "blackhole-preview.glsl"), ("live", "blackhole.glsl")]:
    (root / (name + ".ghostty")).write_text(
        f'custom-shader = {root.as_posix()}/{file}\n'
        'custom-shader-animation = true\nfont-size = 15\ncursor-style-blink = false\n', encoding="utf-8")
command = f'"{Path(sys.executable).as_posix()}" "{root.as_posix()}/claude-token.py"'
settings = {"statusLine": {"type": "command", "command": command}, "hooks": {
    event: [{"hooks": [{"type": "command", "command": command}]}]
    for event in ["SessionStart", "SessionEnd"]}}
(root / "claude-settings.example.json").write_text(json.dumps(settings, indent=2), encoding="utf-8")
print("Generated preview.ghostty, live.ghostty and claude-settings.example.json locally.")
