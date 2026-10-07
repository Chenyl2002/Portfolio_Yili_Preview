"""Verify and extract the approved static preview. No network access or dependencies."""
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import stat
import zipfile

ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / "manifest.json").read_text())
chunks = []
for part in manifest["parts"]:
    name = part["path"]
    if PurePosixPath(name).name != name or not name.startswith("preview.zip.part"):
        raise ValueError("Invalid archive part path")
    data = (ROOT / name).read_bytes()
    if len(data) != part["bytes"] or hashlib.sha256(data).hexdigest() != part["sha256"]:
        raise ValueError("Archive part checksum mismatch: " + name)
    chunks.append(data)
archive = b"".join(chunks)
if len(archive) != manifest["archive_bytes"] or hashlib.sha256(archive).hexdigest() != manifest["archive_sha256"]:
    raise ValueError("Archive checksum mismatch")
destination = ROOT / "dist"
destination.mkdir(exist_ok=False)
with zipfile.ZipFile(io.BytesIO(archive)) as z:
    entries = z.infolist()
    if len(entries) != 1047 or sum(e.file_size for e in entries) > 100_000_000:
        raise ValueError("Unexpected archive size")
    for entry in entries:
        path = PurePosixPath(entry.filename)
        if path.is_absolute() or ".." in path.parts or "\\" in entry.filename or stat.S_ISLNK(entry.external_attr >> 16):
            raise ValueError("Unsafe archive member")
        if any(p in {".git", ".env", ".github", "CNAME"} for p in path.parts):
            raise ValueError("Excluded archive member")
        output = destination.joinpath(*path.parts)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(z.read(entry))
if not (destination / "index.html").is_file():
    raise ValueError("Missing website entry point")
print(f"Verified and extracted {len(entries)} static files")
