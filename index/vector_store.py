"""ChromaDB adapter interface."""


class VectorStore:
    def upsert(self, chunks):
        raise NotImplementedError

    def delete_paths(self, repo: str, paths: list[str]) -> None:
        raise NotImplementedError
