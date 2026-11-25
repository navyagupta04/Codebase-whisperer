"""Citation resolution is intentionally backend-owned, not model-generated."""

from core.schema import Chunk


def github_permalink(chunk: Chunk) -> str:
    owner, name = chunk.repo.split("/", 1)
    return (f"https://github.com/{owner}/{name}/blob/{chunk.commit_sha}/{chunk.path}"
            f"#L{chunk.start_line}-L{chunk.end_line}")


def validate_chunk_ids(ids: list[str], retrieved: list[Chunk]) -> list[str]:
    allowed = {chunk.chunk_id for chunk in retrieved}
    return [chunk_id for chunk_id in ids if chunk_id in allowed]
