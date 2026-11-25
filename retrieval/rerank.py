"""Reranker interface for fused retrieval candidates."""


async def rerank(query: str, candidates: list, limit: int = 8):
    raise NotImplementedError("Candidate reranking is not implemented yet")
