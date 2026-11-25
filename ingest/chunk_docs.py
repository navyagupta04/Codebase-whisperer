"""Heading-aware documentation chunker interface."""

from core.schema import Chunk


def chunk_markdown(repo: str, path: str, text: str, commit_sha: str) -> list[Chunk]:
    """Split Markdown by heading while preserving inclusive source line ranges."""
    raise NotImplementedError("Documentation chunking is not implemented yet")
