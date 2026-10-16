PYTHON ?= python3
VENV := .venv
BIN := $(VENV)/bin

.PHONY: install dev worker test lint format typecheck check migrate migration infra-up infra-down

install:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/python -m pip install --upgrade pip
	$(BIN)/python -m pip install -e '.[dev]'

dev:
	$(BIN)/python -m uvicorn fact_checking_system.main:app --reload --host 0.0.0.0 --port 8000

worker:
	$(BIN)/python -m fact_checking_system.worker

test:
	$(BIN)/python -m pytest

lint:
	$(BIN)/python -m ruff check .

format:
	$(BIN)/python -m ruff format .

typecheck:
	$(BIN)/python -m mypy

check:
	$(BIN)/python -m ruff format --check .
	$(BIN)/python -m ruff check .
	$(BIN)/python -m mypy
	$(BIN)/python -m pytest

migrate:
	$(BIN)/python -m alembic upgrade head

migration:
	@test -n "$(name)" || (echo "usage: make migration name=describe_change"; exit 1)
	$(BIN)/python -m alembic revision --autogenerate -m "$(name)"

infra-up:
	docker compose up -d postgres temporal

infra-down:
	docker compose down

