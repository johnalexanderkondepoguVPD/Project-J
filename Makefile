.PHONY: all help db-up db-down db-migrate db-reset test lint format clean

all: help ## Show this help message

help: ## Show this help message
	@grep -E '^[a-zA-Z_-+]+:?## .+' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":?## "}; {printf "\033[36m  %-15s\033[0m %s\n", $$1, $$2}'

## Frontend
frontend-install: ## Install frontend dependencies
	cd frontend && npm install

frontend-dev: ## Start frontend development server
	cd frontend && npm run dev

frontend-build: ## Build frontend for production
	cd frontend && npm run build

backend-install: ## Install backend dependencies
	cd backend && pip install -r requirements.txt

backend-dev: ## Start backend development server
	cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

db-up: ## Start PostgreSQL and Redis via Docker
	docker-compose up -d postgres redis minio

db-down: ## Stop Docker services
	docker-compose down

db-migrate: ## Run Alembic migrations
	cd backend && python -m alembic upgrade head

db-reset: ## Reset database (drop and recreate)
	docker-compose down
	docker-compose up -d postgres
	cd backend && python -m alembic downgrade base
	cd backend && python -m alembic upgrade head

test: ## Run backend tests
	cd backend && pytest

lint: ## Run linting on backend
	cd backend && ruff check .

format: ## Format backend code
	cd backend && ruff format .

clean: ## Clean up temporary files
	rm -rf **/.pytest_cache
	rm -rf **/.__pycache__
	rm -rf **/htmlcov
	rm -rf frontend/.next

.DEFAULT_GOAL := help