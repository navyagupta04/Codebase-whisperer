"""Code-aware chunker interface. Tree-sitter parsing is a planned implementation."""

from core.schema import Chunk


def chunk_python(repo: str, path: str, text: str, commit_sha: str) -> list[Chunk]:
    """Return function/class chunks with inclusive, 1-based lines (not implemented)."""
    raise NotImplementedError("Tree-sitter code chunking is scheduled for the ingestion milestone")
