# Project-J - AI Government Exam Intelligence Platform

## Overview

Project-J is a full-stack AI-powered Government Examination Intelligence Platform that automatically:
- Discovers government examinations
- Collects previous-year question papers
- Analyzes examination patterns
- Monitors upcoming and ongoing examinations
- Retrieves newly released question papers
- Verifies answers and generates detailed explanations
- Creates AI-powered mock tests

## Technology Stack

### Frontend
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- shadcn/ui
- Lucide React
- React Hook Form
- Zod (validation)
- TanStack Query (data fetching)
- Recharts (data visualization)

### Backend
- Python 3.12+
- FastAPI
- SQLAlchemy 2.x
- Pydantic v2
- PostgreSQL with pgvector
- Alembic (migrations)
- JWT Authentication

### AI / Machine Learning
- OpenAI-compatible LLM integration
- Sentence Transformers
- PyTorch
- PaddleOCR
- PyMuPDF, pdfplumber (PDF processing)
- NumPy, Pandas
- Celery + Redis (background processing)

### Infrastructure
- Docker & Docker Compose
- Redis (cache + broker)
- MinIO (S3-compatible storage)
- GitHub Actions (CI/CD)

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.12+
- Node.js 18+
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/project-j.git
   cd project-j
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start infrastructure services**
   ```bash
   docker-compose up -d
   ```

4. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

5. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   ```

6. **Run database migrations**
   ```bash
   cd backend
   python -m alembic upgrade head
   ```

7. **Start the development servers**
   ```bash
   # In one terminal
   cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   
   # In another terminal
   cd frontend && npm run dev
   ```

## Available Routes

### API Endpoints (FastAPI)
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/v1/` - API v1 base
- Examination management endpoints
- Question paper endpoints
- Mock test endpoints
- Authentication endpoints

### Frontend Routes (Next.js)
- `/` - Home page with examination discovery
- `/examinations` - List of examinations
- `/examinations/[id]` - Examination details
- `/question-papers` - Question paper listing
- `/mock-tests` - Mock test generation

## Documentation

- `docs/architecture/` - System architecture diagrams
- `docs/database/` - Database schema and ER diagrams
- `docs/api/` - API reference documentation
- `docs/modules/` - Module development guides
- `docs/workflows/` - Operational workflows
- `docs/development/` - Development setup guides
- `docs/deployment/` - Deployment guides

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Please read the CONTRIBUTING.md guide for details on code style, testing, and submission guidelines.

## Security

If you discover any security vulnerabilities, please report them following the guidelines in SECURITY.md.