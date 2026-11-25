from urllib.parse import urlparse

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.schema import RepositoryRegistration, RepositoryRegistrationResult

app = FastAPI(title="Codebase Whisperer API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_origin_regex=r"chrome-extension://.*",
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def canonical_public_repo(url: str) -> str | None:
    parsed = urlparse(url.strip())
    if parsed.scheme not in {"http", "https"} or parsed.netloc.lower() not in {"github.com", "www.github.com"}:
        return None
    parts = [part for part in parsed.path.strip("/").split("/") if part]
    if len(parts) < 2:
        return None
    owner, name = parts[:2]
    if owner in {"settings", "login", "orgs", "marketplace", "features"}:
        return None
    name = name.removesuffix(".git")
    if not owner or not name:
        return None
    return f"https://github.com/{owner}/{name}"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "codebase-whisperer"}


@app.post("/repositories/analyse", response_model=RepositoryRegistrationResult)
def analyse_repository(request: RepositoryRegistration) -> RepositoryRegistrationResult:
    canonical = canonical_public_repo(request.url)
    if canonical is None:
        return RepositoryRegistrationResult(
            canonical_url=request.url,
            status="unsupported",
            decision="reject",
            message="Provide a public GitHub repository URL in owner/repository form.",
        )
    return RepositoryRegistrationResult(
        canonical_url=canonical,
        status="pending",
        decision="ingest",
        message="Registration contract is ready; repository ingestion is not connected yet.",
    )
