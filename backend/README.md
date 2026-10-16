# Fact Checking System

Backend foundation for a spec-driven, LLM-assisted fact-checking system.

The repository currently contains infrastructure boilerplate only. The draft [FCS-001 article fact-checking specification](specs/changes/FCS-001-article-fact-checking/README.md) defines the first domain workflow; no article, claim, verdict, or report behavior is implemented yet.

## Stack

- Python 3.13
- FastAPI and Pydantic
- PostgreSQL with SQLAlchemy and Alembic
- Temporal for durable workflows
- Provider-neutral structured LLM interface
- pytest, Ruff, and mypy

## Local setup

```bash
cp .env.example .env
make install
make infra-up
make migrate
make dev
```

The API is available at `http://localhost:8000`, OpenAPI at `http://localhost:8000/docs`, and the local Temporal UI at `http://localhost:8233`.

Run the worker in a second terminal:

```bash
make worker
```

## Quality checks

```bash
make check
```

This runs formatting checks, linting, type checking, and tests.

## Spec-driven workflow

Feature implementation is gated by a reviewed change directory under `specs/changes/`. The first draft change includes a proposal, requirements, design, tasks, and an acceptance plan. Prompt text remains user supplied.

## Project layout

```text
src/fact_checking_system/
  api/          HTTP transport
  db/           persistence infrastructure
  llm/          provider-neutral LLM boundary
  workflows/    Temporal workflow registrations
specs/
  changes/      active specifications
  archive/      completed specifications
tests/          automated tests
```

