"""Static checks for Windows; these do not replace an Xcode build or XCTest."""
from pathlib import Path
import json
import plistlib
import sys
import wave

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "work" / "validation-pydeps"))
import yaml
from tree_sitter import Language, Parser
import tree_sitter_swift

parser = Parser(Language(tree_sitter_swift.language()))
failures = []
swift_files = [ROOT / "Package.swift", *ROOT.glob("MapleMusic/**/*.swift"), *ROOT.glob("MapleMusicTests/*.swift")]
for path in swift_files:
    tree = parser.parse(path.read_bytes())
    if tree.root_node.has_error:
        pending = [tree.root_node]
        while pending:
            node = pending.pop()
            if node.type == "ERROR" or node.is_missing:
                failures.append(f"{path.relative_to(ROOT)}:{node.start_point.row + 1}: {node.type}")
            pending.extend(node.children)

for path in [ROOT / "project.yml", ROOT / "xtool.yml", ROOT / ".github/workflows/build-ipa.yml"]:
    assert isinstance(yaml.safe_load(path.read_text(encoding="utf-8")), dict), path
for path in ROOT.glob("MapleMusic/Resources/**/*.json"):
    json.loads(path.read_text(encoding="utf-8"))
for pattern in ["*.plist", "*.xcprivacy"]:
    for path in ROOT.glob(f"MapleMusic/Resources/{pattern}"):
        plistlib.loads(path.read_bytes())
for path in ROOT.glob("MapleMusic/Resources/DemoAudio/*.wav"):
    with wave.open(str(path)) as audio:
        assert audio.getnchannels() == 1 and audio.getsampwidth() == 2 and audio.getframerate() == 44100
project = yaml.safe_load((ROOT / "project.yml").read_text())
sources = project["targets"]["MapleMusic"]["sources"]
assert any(item["path"] == "MapleMusic/Resources" for item in sources)
assert project["settings"]["base"]["SWIFT_VERSION"] == "5.0"
if failures:
    print("\n".join(failures))
    sys.exit(1)
print(f"PASS: syntax of {len(swift_files)} Swift files; YAML, plists, asset metadata, demo WAVs.")
print("NOT RUN: Swift type checking, iOS simulator, XCTest, device archive or signing.")
