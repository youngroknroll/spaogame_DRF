.PHONY: help install test lint format clean docker-up docker-down migrate shell

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linting"
	@echo "  make format       - Format code"
	@echo "  make clean        - Clean cache files"
	@echo "  make docker-up    - Start Docker services"
	@echo "  make docker-down  - Stop Docker services"
	@echo "  make migrate      - Run migrations"
	@echo "  make shell        - Start Django shell"

install:
	uv sync

test:
	uv run pytest -v

lint:
	uv run ruff check .

format:
	uv run ruff format .
	uv run ruff check --fix .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov

docker-up:
	docker compose up -d

docker-down:
	docker compose down

migrate:
	uv run python manage.py migrate

shell:
	uv run python manage.py shell
