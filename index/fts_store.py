"""SQLite FTS5 keyword index interface."""


class KeywordStore:
    def search(self, query: str, repos: list[str], limit: int = 30):
        raise NotImplementedError
