import sqlite3
from pathlib import Path

SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS repos (
    id TEXT PRIMARY KEY, canonical_url TEXT NOT NULL UNIQUE, owner TEXT NOT NULL,
    name TEXT NOT NULL, default_branch TEXT, indexed_sha TEXT, workspace_id TEXT,
    status TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS chunks (
    chunk_id TEXT PRIMARY KEY, repo_id TEXT NOT NULL REFERENCES repos(id) ON DELETE CASCADE,
    source_type TEXT NOT NULL, path TEXT NOT NULL, symbol TEXT, language TEXT,
    start_line INTEGER NOT NULL, end_line INTEGER NOT NULL, commit_sha TEXT NOT NULL,
    text TEXT NOT NULL, content_hash TEXT NOT NULL, meta_json TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS sync_state (
    repo_id TEXT PRIMARY KEY REFERENCES repos(id) ON DELETE CASCADE,
    last_sha TEXT, last_synced_at TEXT, status TEXT NOT NULL DEFAULT 'pending'
);
CREATE TABLE IF NOT EXISTS pending_actions (
    id TEXT PRIMARY KEY, type TEXT NOT NULL, repo TEXT NOT NULL, payload_json TEXT NOT NULL,
    payload_hash TEXT NOT NULL, status TEXT NOT NULL, created_at TEXT NOT NULL, expires_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT, action_id TEXT, event TEXT NOT NULL,
    actor TEXT NOT NULL, timestamp TEXT NOT NULL, detail TEXT
);
CREATE TABLE IF NOT EXISTS query_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT NOT NULL, repo TEXT,
    retrieved_chunk_ids TEXT NOT NULL DEFAULT '[]', latency_ms INTEGER,
    tokens_in INTEGER, tokens_out INTEGER, cost_usd REAL, created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_chunks_repo_path ON chunks(repo_id, path);
CREATE INDEX IF NOT EXISTS idx_actions_status ON pending_actions(status);
"""


def connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.executescript(SCHEMA)
    return connection
