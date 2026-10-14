PYTHON ?= python3
VENV := .venv
BIN := $(VENV)/bin

.PHONY: install dev worker test lint format typecheck check migrate migration infra-up infra-down

install:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/python -m pip install --upgrade pip
	$(BIN)/python -m pip install -e '.[dev]'

dev:
	$(BIN)/uvicorn fact_checking_system.main:app --reload --host 0.0.0.0 --port 8000

worker:
	$(BIN)/python -m fact_checking_system.worker

test:
	$(BIN)/pytest

lint:
	$(BIN)/ruff check .

format:
	$(BIN)/ruff format .

typecheck:
	$(BIN)/mypy

check:
	$(BIN)/ruff format --check .
	$(BIN)/ruff check .
	$(BIN)/mypy
	$(BIN)/pytest

migrate:
	$(BIN)/alembic upgrade head

migration:
	@test -n "$(name)" || (echo "usage: make migration name=describe_change"; exit 1)
	$(BIN)/alembic revision --autogenerate -m "$(name)"

infra-up:
	docker compose up -d postgres temporal

infra-down:
	docker compose down

