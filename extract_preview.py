"""Reconstruct and verify the static preview offline, using Python's standard library.

Only checksum-pinned baseline bytes and the reviewed delta become public files.
Refuses an existing dist directory and stages all work before publishing it locally.
"""
from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
BASELINE_MANIFEST_SHA256 = "e4bec7ce879d7bfe8d9a3a3c4e578c76b9bbc10896382c5412576f5fcb2fc791"
BASELINE_ARCHIVE_SHA256 = "47ead0992116c8e5bc760b89229c2a1103f0e785033cbca1fbbb72e4472e6254"
BASELINE_COMMIT = "93b16facda9ed4abc903ba749b4e88e4f8ab7afd"
MAX_FILES = 5000
MAX_BYTES = 150_000_000
DELTA_PART_BYTES = 8 * 1024 * 1024
HASH = re.compile(r"[0-9a-f]{64}\Z")
FORBIDDEN_COMPONENTS = {".git", ".github", ".aws", ".codex", "node_modules", "CNAME"}
FORBIDDEN_FILENAMES = {"credentials", "credentials.json", "id_rsa", "id_ed25519", "npmrc", ".npmrc"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def safe_path(name):
    require(isinstance(name, str) and bool(name), "Missing member path")
    path = PurePosixPath(name)
    require(not path.is_absolute() and path.as_posix() == name, "Noncanonical member path: " + name)
    require(not any(p in {"", ".", ".."} for p in name.split("/")), "Unsafe member path: " + name)
    require(not any(ord(c) < 32 or ord(c) == 127 for c in name), "Control character in member path")
    require("\\" not in name and ":" not in name and len(name) <= 512, "Unsafe member path: " + name)
    for part in path.parts:
        require(part not in FORBIDDEN_COMPONENTS and part not in FORBIDDEN_FILENAMES, "Excluded member: " + name)
        require(not part.lower().startswith(".env"), "Environment file is excluded: " + name)
        require(not part.startswith(".") or part == ".nojekyll", "Hidden member is excluded: " + name)
    require(not path.suffix.lower() in {".pem", ".key", ".p12", ".pfx", ".map"}, "Private/source-map member is excluded: " + name)
    return path


def read_regular(root, name, expected_bytes=None, expected_sha256=None):
    path = root / name
    require(path.is_file() and not path.is_symlink(), "Missing or nonregular input: " + name)
    require(path.stat().st_size <= MAX_BYTES, "Input is too large: " + name)
    data = path.read_bytes()
    if expected_bytes is not None:
        require(type(expected_bytes) is int and len(data) == expected_bytes, "Input size mismatch: " + name)
    if expected_sha256 is not None:
        require(isinstance(expected_sha256, str) and HASH.fullmatch(expected_sha256), "Invalid checksum: " + name)
        require(digest(data) == expected_sha256, "Input checksum mismatch: " + name)
    return data


def file_records(root):
    files = []
    for path in sorted(root.rglob("*")):
        require(not path.is_symlink(), "Symlinks are excluded")
        if path.is_dir():
            continue
        require(path.is_file(), "Nonregular output file")
        name = path.relative_to(root).as_posix()
        safe_path(name)
        data = path.read_bytes()
        files.append({"path": name, "bytes": len(data), "sha256": digest(data)})
    return sorted(files, key=lambda record: record["path"])


def records_by_path(records):
    require(isinstance(records, list) and 0 < len(records) <= MAX_FILES, "Invalid output file manifest")
    mapped = {}
    for record in records:
        require(isinstance(record, dict) and set(record) == {"path", "bytes", "sha256"}, "Invalid file record")
        name = record["path"]
        path = safe_path(name)
        require(name not in mapped, "Duplicate manifest member: " + name)
        require(type(record["bytes"]) is int and 0 <= record["bytes"] <= MAX_BYTES, "Invalid file size")
        require(isinstance(record["sha256"], str) and HASH.fullmatch(record["sha256"]), "Invalid file checksum")
        mapped[name] = record
    require(list(mapped) == sorted(mapped), "File manifest must be sorted")
    require(sum(r["bytes"] for r in records) <= MAX_BYTES, "Output exceeds maximum size")
    for name in mapped:
        require(not any(parent.as_posix() in mapped for parent in PurePosixPath(name).parents if parent.as_posix() != "."), "File/directory collision")
    return mapped


def validated_archive(data):
    archive = zipfile.ZipFile(io.BytesIO(data))
    entries = archive.infolist()
    require(len(entries) <= MAX_FILES and sum(e.file_size for e in entries) <= MAX_BYTES, "Archive exceeds maximum size")
    names = set()
    for entry in entries:
        safe_path(entry.filename)
        require(entry.filename not in names, "Duplicate archive member: " + entry.filename)
        names.add(entry.filename)
        mode = entry.external_attr >> 16
        require(not entry.is_dir() and stat.S_IFMT(mode) in {0, stat.S_IFREG}, "Nonregular archive member")
        require(not entry.flag_bits & 1, "Encrypted archive member")
        require(entry.compress_type in {zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED}, "Unsupported compression")
        require(0 <= entry.file_size <= MAX_BYTES, "Invalid member size")
    for name in names:
        require(not any(parent.as_posix() in names for parent in PurePosixPath(name).parents if parent.as_posix() != "."), "Archive file/directory collision")
    return archive


def archive_records(archive):
    return sorted(
        [{"path": e.filename, "bytes": e.file_size, "sha256": digest(archive.read(e))} for e in archive.infolist()],
        key=lambda record: record["path"],
    )


def write_members(archive, destination):
    for entry in archive.infolist():
        output = destination.joinpath(*PurePosixPath(entry.filename).parts)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(archive.read(entry))


def load_baseline(root):
    raw = read_regular(root, "manifest.json", expected_sha256=BASELINE_MANIFEST_SHA256)
    manifest = json.loads(raw)
    require(manifest["archive_sha256"] == BASELINE_ARCHIVE_SHA256, "Unexpected baseline archive")
    chunks = []
    for i, part in enumerate(manifest["parts"]):
        require(part["path"] == f"preview.zip.part{i:02d}", "Invalid baseline part order")
        chunks.append(read_regular(root, part["path"], part["bytes"], part["sha256"]))
    data = b"".join(chunks)
    require(len(data) == manifest["archive_bytes"] and digest(data) == BASELINE_ARCHIVE_SHA256, "Baseline archive mismatch")
    archive = validated_archive(data)
    require(len(archive.infolist()) == 1047, "Unexpected baseline file count")
    return archive


def load_delta(root, info):
    """Read exactly one schema-1 delta representation, validating before extraction."""
    require(isinstance(info, dict), "Invalid delta metadata")
    common = {"bytes", "sha256", "file_count"}
    require(set(info) in (common | {"path"}, common | {"parts"}), "Ambiguous or invalid delta representation")
    require(type(info["bytes"]) is int and 0 < info["bytes"] <= MAX_BYTES, "Invalid delta total size")
    require(isinstance(info["sha256"], str) and HASH.fullmatch(info["sha256"]), "Invalid delta checksum")
    require(type(info["file_count"]) is int and 0 <= info["file_count"] <= MAX_FILES, "Invalid delta file count")
    actual_parts = {p.name for p in root.glob("preview-delta.zip.part*")}
    if "path" in info:
        require(info["path"] == "preview-delta.zip", "Unexpected delta path")
        require(not actual_parts, "Unexpected delta parts for single archive")
        return read_regular(root, info["path"], info["bytes"], info["sha256"])
    require(not (root / "preview-delta.zip").exists() and not (root / "preview-delta.zip").is_symlink(), "Unexpected single delta alongside parts")
    parts = info["parts"]
    count = (info["bytes"] + DELTA_PART_BYTES - 1) // DELTA_PART_BYTES
    require(isinstance(parts, list) and len(parts) == count, "Delta part count mismatch")
    expected_names = {f"preview-delta.zip.part{i:02d}" for i in range(count)}
    require(actual_parts == expected_names, "Delta part set mismatch")
    chunks = []
    for i, part in enumerate(parts):
        require(isinstance(part, dict) and set(part) == {"path", "bytes", "sha256"}, "Invalid delta part metadata")
        require(part["path"] == f"preview-delta.zip.part{i:02d}", "Invalid delta part path/order")
        expected_size = min(DELTA_PART_BYTES, info["bytes"] - i * DELTA_PART_BYTES)
        require(type(part["bytes"]) is int and part["bytes"] == expected_size, "Invalid delta part size")
        path = root / part["path"]
        require(path.is_file() and not path.is_symlink(), "Missing or nonregular delta part")
        require(path.stat().st_size == expected_size, "Delta part actual size mismatch")
        chunks.append(read_regular(root, part["path"], part["bytes"], part["sha256"]))
    data = b"".join(chunks)
    require(len(data) == info["bytes"] and digest(data) == info["sha256"], "Combined delta archive mismatch")
    return data


def load_release_json(raw):
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "Duplicate JSON key: " + key)
            result[key] = value
        return result
    def invalid_constant(value):
        raise ValueError("Non-finite JSON constant: " + value)
    release = json.loads(raw, object_pairs_hook=unique_object, parse_constant=invalid_constant)
    require(isinstance(release, dict), "Invalid release manifest")
    return release


def main(root=ROOT):
    root = Path(root).resolve()
    destination = root / "dist"
    require(not destination.exists() and not destination.is_symlink(), "dist must not exist; run from a clean checkout")
    release = load_release_json(read_regular(root, "release-manifest.json"))
    require(type(release.get("schema")) is int and release["schema"] == 1 and release["baseline_commit"] == BASELINE_COMMIT, "Unsupported release baseline")
    require(release["baseline_archive_sha256"] == BASELINE_ARCHIVE_SHA256, "Unexpected release baseline checksum")
    baseline = load_baseline(root)
    baseline_files = records_by_path(archive_records(baseline))
    expected_records = release["output"]["files"]
    expected = records_by_path(expected_records)
    require(digest(canonical_json(expected_records)) == release["output"]["tree_sha256"], "Output manifest checksum mismatch")
    require(len(expected) == release["output"]["file_count"], "Output file count mismatch")
    require(sum(f["bytes"] for f in expected_records) == release["output"]["total_bytes"], "Output total size mismatch")
    require("index.html" in expected, "Missing website entry point")
    for name, record in baseline_files.items():
        if name.startswith("licenses/") or name == "fonts/OFL-notice.txt":
            require(expected.get(name) == record, "Baseline licensing must remain unchanged: " + name)
    removed = sorted(set(baseline_files) - set(expected))
    require(release["removed"] == removed, "Deletion set mismatch")
    changes = sorted(name for name, record in expected.items() if baseline_files.get(name) != record)
    delta_info = release["delta"]
    delta_bytes = load_delta(root, delta_info)
    delta = validated_archive(delta_bytes)
    changed_records = archive_records(delta)
    require(changed_records == [expected[name] for name in changes], "Delta file set/content mismatch")
    require(delta_info["file_count"] == len(changes), "Delta file count mismatch")
    staging = Path(tempfile.mkdtemp(prefix=".preview-stage-", dir=root))
    try:
        write_members(baseline, staging)
        for name in removed:
            (staging / name).unlink()
        # A removed file may become a directory, or vice versa. Remove empty dirs first.
        for directory in sorted((p for p in staging.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
            if not any(directory.iterdir()):
                directory.rmdir()
        write_members(delta, staging)
        actual = file_records(staging)
        require(actual == expected_records, "Reconstructed output differs from approved output manifest")
        require(not destination.exists() and not destination.is_symlink(), "dist appeared during extraction")
        staging.rename(destination)
    finally:
        baseline.close()
        delta.close()
        if staging.exists():
            shutil.rmtree(staging)
    print(json.dumps({"verified": True, "files": len(expected), "bytes": release["output"]["total_bytes"], "tree_sha256": release["output"]["tree_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
