# Codebase Whisperer

Codebase Whisperer is a repository-aware assistant planned for the PS-04 RAG and MCP hackathon track. Its goal is to help a developer understand an unfamiliar public GitHub repository through answers grounded in code, documentation, issues, pull requests, and commit history. Answers are designed to cite exact source ranges, mark claims as verified or inferred, and say when the indexed repository does not contain the answer.

This repository is the **starter scaffold**, not a completed implementation of the project plan. The API and UI shells and the browser-extension popup are present. Most ingestion, indexing, retrieval, sync, evaluation, onboarding, and MCP workflows remain implementation work. The placeholders in those modules raise `NotImplementedError` where applicable so unfinished integrations are visible.

## Contents

- [Project goals and scope](#project-goals-and-scope)
- [Architecture](#architecture)
- [Repository layout](#repository-layout)
- [Requirements](#requirements)
- [Quick start](#quick-start)
- [Configuration](#configuration)
- [Run the application](#run-the-application)
- [Browser extension](#browser-extension)
- [API endpoints](#api-endpoints)
- [Data and answer contracts](#data-and-answer-contracts)
- [Safety principles](#safety-principles)
- [Implementation status](#implementation-status)
- [Planned delivery sequence](#planned-delivery-sequence)
- [Evaluation plan](#evaluation-plan)
- [Contributing](#contributing)

## Project goals and scope

The core product path is: register a public repository, build an index, ask a question, inspect validated citations, and optionally propose a GitHub action for a person to review. The planned core includes:

1. Public GitHub repository registration and ingestion of source, docs, issues, pull requests, and commits.
2. Code-aware chunks with exact 1-based inclusive line ranges and commit-SHA metadata.
3. Hybrid retrieval using vector and keyword search, rank fusion, and reranking.
4. Cited answers with per-claim verified/inferred labels and explicit not-found responses.
5. Role- and skill-aware onboarding guides with cited sections and suggested first issues.
6. MCP-backed issue and pull-request proposals gated by a human approval workflow.
7. Incremental synchronization that updates changed, renamed, and deleted paths.
8. A labelled evaluation set and reported retrieval, citation, faithfulness, and not-found metrics.
9. A Chrome/Edge Manifest V3 extension that detects a public GitHub repository and opens its workspace.

Multi-repository search, multilingual answers, and change summaries are stretch goals. A GitHub side-panel assistant that reads active-page context is future scope. The app is not intended to execute repository code or run a repository's test suite. Private-repository authentication, multi-user accounts, production deployment, and fine-tuning are outside the current hackathon scope.

## Architecture

```text
Chrome / Edge popup
        | POST /repositories/analyse
        v
     FastAPI  <-------------------------->  Streamlit workspace
        |                                      Chat / onboarding /
        |                                      pending actions / eval
        v
 Repository registration and ingestion
        | code + docs + issues + PRs + commits
        v
 Chunkers --> Chroma vector index + SQLite FTS5 keyword index
        |                         |
        +---- Hybrid retrieval (RRF) + reranking
                                  |
                         Cited answer agent
                                  |
                     citation validation / not found

 Sync worker --> changed paths --> index updates
 MCP proposal --> pending action --> human review --> GitHub write
                                   (approval gate)
```

### Planned technology choices

| Layer | Planned choice | Purpose |
| --- | --- | --- |
| Language | Python 3.11 | Application and data pipeline |
| HTTP API | FastAPI | Registration, query, sync, and approval endpoints |
| UI | Streamlit | Chat workspace and review/evaluation tabs |
| Code parsing | Tree-sitter | Function/class chunks and accurate source lines |
| Embeddings | OpenAI embeddings | Semantic retrieval |
| Vector index | ChromaDB | Local persistent vector search |
| Keyword index | SQLite FTS5 | Keyword search without a separate service |
| GitHub access | REST API, HTTPX, GitPython | Public repository content and controlled actions |
| MCP | Official Python MCP SDK | Repository lookup and proposal tools |
| Scheduling | APScheduler | Periodic sync polling |
| Browser extension | Chrome/Edge Manifest V3 | One-click repository entry point |

Model identifiers and prices change. Choose models for each role through environment configuration and confirm current pricing before running bulk indexing or evaluation.

## Repository layout

```text
.
├── agent/              Answer prompt, citation, not-found, and Q&A seams
├── api/                FastAPI application and repository registration contract
├── browser_extension/  Manifest V3 popup (HTML, CSS, JavaScript)
├── core/               Settings, Pydantic schemas, SQLite table definitions
├── eval/               Evaluation dataset format and metric/report seams
├── index/              Embedding, vector-store, and FTS interfaces
├── ingest/             File discovery and code/docs/GitHub chunking seams
├── mcp_server/         MCP tools, approval workflow, and audit seams
├── onboarding/         Developer profile and guide-generation seam
├── retrieval/          Hybrid retrieval, reranking, and stub interface
├── summaries/          Change summaries (stretch goal)
├── sync/               Incremental sync, scheduler, and webhook seams
├── tests/              Test package placeholder
├── ui/                 Streamlit workspace shell
├── .env.example        Local configuration template
├── pyproject.toml       Package metadata and development tooling
└── requirements.txt    Runtime dependency list
```

## Requirements

- Python 3.11 (the package metadata allows Python 3.11 and 3.12).
- Git.
- An OpenAI API key for future embedding and model integrations.
- A GitHub token only for authenticated API access or write operations. Public repository reading can start without a token, subject to GitHub rate limits.
- Chrome or Edge only if you want to load the unpacked extension.

Install the complete runtime dependency set with:

```powershell
python -m pip install -r requirements.txt
```

For development tooling, install the optional development dependencies declared in `pyproject.toml`:

```powershell
python -m pip install -e ".[dev]"
```

## Quick start

From the project root in PowerShell:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and provide credentials when implementing or using integrations that need them. Do not commit `.env`, tokens, API keys, repository contents, local indexes, or logs. These paths are excluded in `.gitignore`.

Start the API and UI in separate terminals:

```powershell
uvicorn api.main:app --reload
```

```powershell
streamlit run ui/app.py
```

The API is served at `http://localhost:8000`; its interactive OpenAPI page is `http://localhost:8000/docs`. Streamlit normally serves the UI at `http://localhost:8501`.

At this scaffold stage, `/health` returns service status and `/repositories/analyse` validates and canonicalizes a GitHub URL. The registration endpoint reports that indexing is pending; it does not clone or index the repository yet. The UI is a navigation shell and does not answer questions yet.

## Configuration

Copy `.env.example` to `.env`. Settings are loaded by `core/config.py` using Pydantic Settings.

| Variable | Purpose | Current default |
| --- | --- | --- |
| `OPENAI_API_KEY` | Model and embedding calls | Empty |
| `GITHUB_TOKEN` | Authenticated GitHub API access | Empty |
| `DATABASE_PATH` | SQLite metadata database | `data/codebase_whisperer.sqlite3` |
| `WORKSPACES_DIR` | Local repository workspace root | `data/workspaces` |
| `CHROMA_DIR` | Persistent Chroma index root | `data/chroma` |
| `ALLOWED_REPOS` | Comma-separated GitHub repo allowlist for writes | Empty |
| `ANSWER_MODEL` | Model role for answer generation | `gpt-4o-mini` |
| `RERANK_MODEL` | Model role for reranking | `gpt-4o-mini` |
| `GUIDE_MODEL` | Model role for onboarding | `gpt-4o` |
| `OPENAI_BUDGET_USD` | Intended project spend limit | `30` |
| `API_BASE_URL` | API URL used by integrations | `http://localhost:8000` |

These variables establish configuration points; most model and GitHub integrations are not implemented yet. Keep credentials local and use a personal fork or test repository for any future GitHub writes.

## Run the application

### FastAPI

```powershell
uvicorn api.main:app --reload
```

Available starter routes:

- `GET /health` — basic liveness response.
- `POST /repositories/analyse` — accepts `{"url":"https://github.com/owner/repository"}` and returns the canonical URL and a pending/rejected registration result.

Example:

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://localhost:8000/repositories/analyse `
  -ContentType 'application/json' `
  -Body '{"url":"https://github.com/pallets/flask"}'
```

### Streamlit

```powershell
streamlit run ui/app.py
```

The initial UI contains Chat, Onboarding, Changes, Pending Actions, and Eval tabs. They currently describe the planned workflows and remain disabled or informational until their backend features are connected.

## Browser extension

The extension is an early popup shell. It reads the active tab URL, recognizes `github.com/owner/repository`, and sends the URL to the local registration endpoint. Since the endpoint currently returns a pending result, actual indexing and workspace navigation are not available yet.

To load it in Chrome or Edge:

1. Start the local API.
2. Open the browser's extensions page and enable Developer mode.
3. Choose **Load unpacked** and select this repository's `browser_extension/` directory.
4. Open a public GitHub repository and click the Codebase Whisperer extension.

The extension host permission is scoped to `http://localhost:8000/*`. Update the manifest and API CORS settings together if the development API moves to another origin. Do not add broad permissions unless the product requires them.

## API endpoints

### `GET /health`

Returns a simple JSON health response, for example:

```json
{"status":"ok","service":"codebase-whisperer"}
```

### `POST /repositories/analyse`

Request body:

```json
{"url":"https://github.com/owner/repository"}
```

The current handler accepts GitHub repository-shaped URLs and canonicalizes them to `https://github.com/owner/repository`. It does not yet verify repository visibility, check the registry, start ingestion, or return an existing workspace. Those behaviors are part of the planned repository-registration implementation.

## Data and answer contracts

### Chunk

`core/schema.py` defines the shared chunk shape: stable chunk ID, repository, source type, path, optional symbol/language, inclusive start/end lines, indexed commit SHA, text, content hash, and source metadata. Source types are `code`, `doc`, `issue`, `pr`, and `commit`.

### Retrieval

The planned interface is:

```python
retrieve(query, repos, source_types=None, k=8) -> list[ScoredChunk]
```

Each result carries a score and a trace containing vector rank, keyword rank, and rerank score. The current `retrieval/stub.py` returns an empty result; `retrieval/hybrid.py` is not implemented.

### Agent answers and citations

The answer contract contains claims with `text`, `type` (`verified` or `inferred`), and retrieved `chunk_ids`, plus `not_found` and optional `missing_info`. The model must never author line numbers. The backend should resolve only retrieved IDs into source paths, line ranges, and GitHub permalinks at the indexed SHA. Invalid IDs must be rejected, and a verified claim without valid evidence must be downgraded or rejected.

### SQLite metadata

`core/db.py` initializes tables for repositories, chunks, sync state, pending actions, audit events, and query logs. Embeddings, FTS synchronization, lifecycle APIs, and migrations have not yet been connected.

## Safety principles

- Treat repository text, issues, and pull-request content as untrusted input.
- Do not execute repository code or run repository-provided scripts as part of ingestion.
- Keep credentials in environment variables or a local secret store, never in source control.
- Restrict future GitHub writes to an explicit allowlist, preferably a personal fork or test repository.
- MCP proposal tools should only create a preview and pending-action record. A separate human approval request must re-check the payload and target allowlist before execution.
- Audit proposed, approved, rejected, and executed actions.
- Validate webhook signatures before accepting GitHub webhook events.
- Enforce a usage budget and cache model responses before bulk indexing.

These are design requirements; the approval executor, webhook validation, and most action logging are not implemented in this scaffold.

## Implementation status

| Area | Present in scaffold | Remaining work |
| --- | --- | --- |
| Configuration and shared schemas | Settings and Pydantic data contracts | Validate runtime settings and add migrations |
| SQLite | Initial table definitions | Repository operations and lifecycle transitions |
| File walking | Basic size and directory filters | Language detection, test tags, and symlink policy |
| Code/docs chunking | Module interfaces | Tree-sitter symbols, Markdown/RST headings, line-range coverage |
| GitHub ingestion | Module seam | Public API pagination, caching, issues, PRs, comments, commits |
| Indexing | Adapter interfaces | Embeddings, Chroma upserts/deletes, SQLite FTS5 |
| Retrieval | Empty stub and interface | Vector/keyword fusion, RRF, rerank, filters, trace |
| Cited Q&A | Prompt and data contracts | LLM wrapper, context assembly, validator, streaming UI |
| Registration API | URL canonicalization and route | Public/unsupported checks, registry lookup, queuing, reuse, status |
| UI | Streamlit tab shell | Repository selection, chat, citations, guide, action and eval views |
| Approval flow | Data table and module seams | Pending state machine, payload hash, expiry, allowlist, executor, audit |
| Sync | Module seams | Git diff, rename/delete handling, partial reindex, scheduler |
| Evaluation | Empty dataset shape and metric interfaces | Label 60 questions, compute/report metrics, analyze failures |
| Onboarding | Developer profile schema | Targeted retrieval, cited guide sections, issue recommendations |
| Extension | Popup URL detection and API call | API integration, statuses, workspace navigation, browser validation |

## Planned delivery sequence

The project plan schedules an eight-day implementation across two developers:

1. **Foundations and contracts:** repository registry, database, chunk schema, file walker, API/UI shells.
2. **Indexing and first answers:** dynamic ingestion, embeddings, FTS, hybrid retrieval, citation plumbing.
3. **Integration and reranking:** repository reuse/status, reranking, not-found handling, first eval questions.
4. **Evaluation and tuning:** 60-question dataset, retrieval/answer metrics, baseline and tuned reports.
5. **Approval and sync:** MCP proposal flow, human review, audit records, incremental update engine.
6. **Onboarding:** TODO scan, good-first-issue ranking, role-aware guide generation.
7. **Extension and polish:** new and existing repository flows, extension errors, regression pass.
8. **Hardening and submission:** fresh setup, final evaluation, demo rehearsal, cost review, backup video.

The README reflects the current starter code, not a claim that these milestones have been completed.

## Evaluation plan

The planned `eval/dataset.json` contains 60 questions: 20 code lookup, 10 documentation, 10 issue/commit “why” questions, 10 cross-file architecture questions, and 10 unanswerable questions. Gold answers include file paths and line ranges.

Planned metrics are Recall@1/3/5/10, mean reciprocal rank, citation precision (range overlap), faithfulness, and not-found accuracy. Initial targets in the project plan are Recall@5 ≥ 0.80, MRR ≥ 0.60, citation precision ≥ 0.85, faithfulness ≥ 0.90, and not-found accuracy ≥ 0.80. No results should be claimed until the dataset is labelled and the evaluation runs are implemented and reviewed.

## Contributing

- Keep feature changes small and align shared interfaces before integrating parallel modules.
- Preserve exact 1-based inclusive source ranges and indexed commit SHA metadata.
- Add focused tests for validators, URL normalization, sync rename/delete behavior, and approval state transitions as those features are implemented.
- Keep secrets, local indexes, repository checkouts, logs, and generated evaluation output out of Git.
- Do not claim a feature is complete until its integration path and acceptance criteria are met.

See the PS-04 project plan for full acceptance criteria, phase assignments, demo flow, risks, and deliverables.
