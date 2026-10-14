# Fact Checking System

Backend foundation for a spec-driven, LLM-assisted fact-checking system.

The repository currently contains infrastructure boilerplate only. Domain behavior must begin with a reviewed change under `specs/changes/`; no article, claim, verdict, or report behavior is implemented yet.

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

Feature implementation is gated by a change directory under `specs/changes/`. The directory is intentionally empty at project setup time. A future change can introduce its own proposal, requirements, design, tasks, and verification evidence before domain code is added.

## Project layout

```text
src/fact_checking_system/
  api/          HTTP transport
  db/           persistence infrastructure
  llm/          provider-neutral LLM boundary
  workflows/    Temporal workflow registrations
specs/
  changes/      active specifications (currently empty)
  archive/      completed specifications
tests/          automated tests
```

