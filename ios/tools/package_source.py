"""Package only the custom client, never the original IPA or local credentials."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib

root = Path(__file__).resolve().parents[1]
destination = root / "dist" / "MapleMusic-source.zip"
destination.parent.mkdir(exist_ok=True)
files = []
for name in ["MapleMusic", "MapleMusicTests", "docs", ".github"]:
    files.extend(p for p in (root / name).rglob("*") if p.is_file())
for name in ["README.md", "project.yml", "Package.swift", "xtool.yml", ".gitignore",
             "Config/App.xcconfig", "Config/Local.example.xcconfig",
             "tools/generate_app_resources.py", "tools/validate_source.py", "tools/package_source.py"]:
    files.append(root / name)
with ZipFile(destination, "w", ZIP_DEFLATED, compresslevel=9) as archive:
    for path in sorted(files):
        archive.write(path, "MapleMusic/" + path.relative_to(root).as_posix())
with ZipFile(destination) as archive:
    assert archive.testzip() is None
print(destination)
print(f"{len(files)} files; SHA256 {hashlib.sha256(destination.read_bytes()).hexdigest()}")
