# Codebase Whisperer

Codebase Whisperer indexes a public GitHub repository so developers can ask questions about its code, documentation, issues, pull requests, and commit history. Answers are designed to cite indexed evidence, distinguish verified claims from inferences, and say when the repository does not contain an answer. Repository actions are proposed for human review before execution.

This repository contains the initial application structure for the PS-04 project plan. The ingestion, persistent indexing, retrieval, sync, evaluation, onboarding, MCP actions, and extension integration modules are scaffolded as explicit seams; they are not represented as completed features yet.

## Project structure

```text
core/                 Configuration, shared schemas, and SQLite metadata
ingest/               Repository walking and code/document/GitHub chunking
index/                Embedding, vector, and keyword index interfaces
retrieval/            Hybrid retrieval, reranking, and a fixture-backed stub
sync/                 Incremental sync and scheduling seams
agent/                Answer contracts, citations, and not-found behavior
mcp_server/           Proposed actions, approval workflow, and audit seam
onboarding/            Personalised guide generation seam
summaries/             Change summary seam (stretch goal)
api/                   FastAPI application and repository registration routes
ui/                    Streamlit application shell
browser_extension/     Manifest V3 popup for repository detection
eval/                  Dataset format and metric/report seams
tests/                 Future unit and integration tests
```

## Local setup

Requires Python 3.11. From the repository root:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[rag,mcp,dev]"
Copy-Item .env.example .env
```

Set the required API keys in `.env` before connecting model or GitHub integrations. Never commit secrets. The default API currently exposes health and registration-contract endpoints; indexing and answer generation require subsequent implementation.

Run the API and UI in separate terminals:

```powershell
uvicorn api.main:app --reload
streamlit run ui/app.py
```

The API docs are available at `http://localhost:8000/docs` while the server runs. Load the unpacked extension from `browser_extension/` in Chrome or Edge developer mode. The popup detects a public `github.com/owner/repository` tab and displays the registration request result; connecting it to a running API is the next integration step.

## Initial design contracts

- Chunk line numbers are 1-based and inclusive. Chunk IDs are stable hashes of repository, path, symbol, and content hash.
- `retrieve(query, repos, source_types=None, k=8)` returns scored chunks with retrieval trace metadata.
- Agent claims reference retrieved chunk IDs. The backend resolves those IDs into path, line range, and a permalink at the indexed commit.
- Propose operations create pending actions only. Approval and rejection are explicit API operations; the model does not execute write actions.
- GitHub write actions must be limited to configured allowlisted repositories, such as a personal fork or test repository.

## Scope from PS-04

The first milestone focuses on public-repository registration, ingestion, cited Q&A, onboarding, approval-gated actions, incremental sync, evaluation, and one-click extension ingestion. Multi-repository search, multilingual output, and change summaries are stretch goals. The in-GitHub side-panel assistant is future scope. The application must not execute repository code or test suites.
