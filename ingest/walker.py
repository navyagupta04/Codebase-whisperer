"""Safe repository file discovery; repository code is never executed."""

from pathlib import Path

SKIP_DIRS = {".git", ".venv", "node_modules", "vendor", "dist", "build", "__pycache__"}
MAX_FILE_BYTES = 1_000_000


def iter_source_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.parts):
            continue
        try:
            if path.stat().st_size <= MAX_FILE_BYTES:
                yield path
        except OSError:
            continue
