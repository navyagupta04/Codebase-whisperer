"""Audit trail writer interface for action lifecycle transitions."""


def record_event(action_id: str, event: str, actor: str, detail: str | None = None) -> None:
    raise NotImplementedError("Action audit logging is not implemented yet")
