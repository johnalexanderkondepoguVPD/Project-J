# Contributing to Project-J

## Development Setup

1. Fork the repository and clone locally
2. Run `cp .env.example .env` and configure your environment variables
3. Start infrastructure: `docker-compose up -d`
4. Install dependencies: `make backend-install` and `make frontend-install`
5. Run migrations: `make db-migrate`
6. Start development servers: `make backend-dev` and `make frontend-dev`

## Code Style

### Python
- Follow [PEP 8](https://pep8.org/) style guidelines
- Use type hints for all function signatures
- Document modules with docstrings
- Run `make lint` and `make format` before committing

### TypeScript/React
- Follow the [Next.js App Router](https://nextjs.org/docs/app) conventions
- Use Tailwind CSS for styling
- Components should be functional with hooks
- Use Zod for runtime validation
- Run `npm run lint` before committing

## Git Workflow

1. Create a branch from `main`: `git checkout -b feature/foo-feature`
2. Make your changes and commit with descriptive messages
3. Push to your fork and create a Pull Request
4. Ensure all tests pass (`make test`)
5. Address any review feedback

## Adding New Features

1. Add corresponding models in `backend/app/Models/`
2. Add Pydantic schemas in `backend/app/schemas/`
3. Add API routes in `backend/app/api/v1/`
4. Add database migrations: `cd backend && alembic revision --autogenerate -m "description"`
5. Add frontend components in `frontend/app/` and `frontend/components/`
6. Update documentation as needed

## Testing

### Backend
- Run all tests: `make test`
- Run specific test file: `cd backend && pytest tests/ -k "test_name"`
- Ensure coverage is maintained

### Frontend
- Run Vitest: `cd frontend && npm test`
- Run E2E tests: `cd frontend && npm run test:e2e`

## Branch Naming Conventions
- Features: `feature/feature-name`
- Bug fixes: `bug/bug-description`
- Refactoring: `refactor/description`
- Documentation: `docs/documentation-name`