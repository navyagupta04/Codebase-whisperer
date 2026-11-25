from core.schema import AgentAnswer


def not_found_answer(missing_info: str | None = None) -> AgentAnswer:
    return AgentAnswer(not_found=True, missing_info=missing_info or "No matching repository evidence was found.")
