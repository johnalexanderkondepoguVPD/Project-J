from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from .core.config import settings
from .core.exceptions import ProjectJException
from .api.v1.auth import router as auth_router
from .api.v1.examination import router as examination_router

API_DESCRIPTION = """
# 🚀 Project-J API
**AI-Powered Government Examination Intelligence Platform**

Welcome to the Project-J REST API documentation. Project-J collects official government exam notifications, organizes previous-year question papers, analyzes historical trends, and delivers verified AI explanations and mock tests.

---

### 🔐 Authentication Guide
This API supports two secure authentication modes:
1. **HTTP-Only Session Cookie (Web Browser)**: When you call `/api/v1/auth/login` or `/api/v1/auth/register`, the server sets an HTTP-only, SameSite cookie (`project_j_session`). Subsequent requests automatically include this cookie.
2. **Bearer Token (Swagger UI / API Clients)**: For direct API testing, scripts, and Swagger UI, you can pass the session token using the `Authorization: Bearer <session_id>` header.

> **Testing in Swagger**: Click the **Authorize 🔓** button below and enter your `session_id` into the **BearerAuth** field.
"""

TAGS_METADATA = [
    {
        "name": "Authentication",
        "description": "User registration, login, session token validation, and account credentials lifecycle.",
    },
    {
        "name": "System",
        "description": "Health checks, system readiness, and operational status.",
    },
    {
        "name": "Examination Catalog",
        "description": "Exam bodies (UPSC, SSC, IBPS, RRB), exams catalog, and examination schedules.",
    },
    {
        "name": "Question Papers",
        "description": "Previous-year question papers archive, official answer keys, and OCR document processing.",
    },
    {
        "name": "Mock Tests",
        "description": "AI-generated and official practice mock tests, attempt sessions, and scoring.",
    },
    {
        "name": "Pattern Analytics",
        "description": "Historical topic frequency, weightage breakdown, and trend analysis.",
    },
]

app = FastAPI(
    title="Project-J API",
    version=settings.app_version,
    description=API_DESCRIPTION,
    openapi_tags=TAGS_METADATA,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_parameters={
        "persistAuthorization": True,
        "displayRequestDuration": True,
        "filter": True,
        "tryItOutEnabled": True,
    },
)


@app.exception_handler(ProjectJException)
async def project_j_exception_handler(request: Request, exc: ProjectJException):
    return JSONResponse(
        status_code=exc.code,
        content={"detail": exc.detail},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins or ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Versioned API route mount
app.include_router(auth_router, prefix="/api/v1")
app.include_router(examination_router, prefix="/api/v1")

# Alias mounts without prefix for convenience
app.include_router(auth_router)
app.include_router(examination_router)


@app.get(
    "/",
    tags=["System"],
    summary="API Root",
    description="Returns basic application status and version metadata.",
)
async def root():
    return {
        "message": "Project-J API",
        "version": settings.app_version,
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    }


@app.get(
    "/health",
    tags=["System"],
    summary="Health Check",
    description="Liveness probe to confirm backend service is running and responsive.",
)
async def health_check():
    return {"status": "healthy", "service": "backend"}


def custom_openapi():
    """Enhance OpenAPI schema with security definitions for Swagger UI."""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=app.openapi_tags,
    )

    # Add security schemes for Swagger Authorize dialog
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "session_id",
            "description": "Enter the 64-character session ID obtained from /auth/login or /auth/register.",
        },
        "CookieAuth": {
            "type": "apiKey",
            "in": "cookie",
            "name": settings.session_cookie_name,
            "description": "Session cookie sent automatically by browsers.",
        },
    }

    # Attach BearerAuth security requirement to protected endpoints
    paths = openapi_schema.get("paths", {})
    for path, path_item in paths.items():
        if path.endswith("/auth/me") and "get" in path_item:
            path_item["get"]["security"] = [{"BearerAuth": []}, {"CookieAuth": []}]
        # Mark mutating /exams endpoints as requiring authentication
        if "/exams" in path:
            for method in ["post", "put", "delete"]:
                if method in path_item and not path.endswith("/seed/initial"):
                    path_item[method]["security"] = [{"BearerAuth": []}, {"CookieAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
