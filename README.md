# Fact Checking System

Monorepo for the fact-checking product.

## Projects

- [`backend/`](backend/README.md) — FastAPI, PostgreSQL, Temporal, and the active fact-checking specifications.
- [`frontend/`](frontend/README.md) — Next.js web application using TypeScript, App Router, Tailwind CSS, and pnpm.

The backend domain workflow is still specification-first. The draft [FCS-001 article fact-checking specification](backend/specs/changes/FCS-001-article-fact-checking/README.md) defines the planned behavior, while the current application code remains infrastructure-only.

## Setup

Install both projects:

```bash
make install
```

Run the backend API and frontend in separate terminals:

```bash
make backend-dev
make frontend-dev
```

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- Backend OpenAPI: `http://localhost:8000/docs`

PostgreSQL, Temporal, migrations, and the backend worker are documented in [`backend/README.md`](backend/README.md).

## Checks

```bash
make check
```

This runs the backend formatter, linter, type checks, and tests, followed by the frontend linter, type checks, and production build.
