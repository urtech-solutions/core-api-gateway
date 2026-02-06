PYTHON ?= python3
PIP ?= pip3

.PHONY: install install-dev lint test run build-docker

install:
	$(PIP) install .

install-dev:
	$(PIP) install -e .[dev]

lint:
	ruff check .

test:
	pytest

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

build-docker:
	docker build -t core-api-gateway:latest .
