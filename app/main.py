import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.api import api_router
from app.core.config import settings
from app.middleware.cloudinary_middleware import configure_cloudinary


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_cloudinary()

    try:
        import firebase_admin
        from firebase_admin import credentials

        if not firebase_admin._apps:
            cred = credentials.Certificate(json.loads(settings.FIREBASE_CREDENTIALS))
            firebase_admin.initialize_app(cred)
    except Exception as exc:
        app.state.firebase_warning = str(exc)

    yield


app = FastAPI(
    lifespan=lifespan,
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
    title="Atlas Music API",
    summary=(
        "Backend API for user management, song metadata, favorites, "
        "recent listens, notifications, and media uploads."
    ),
    description=(
        "A FastAPI backend for music applications with auth, song management, "
        "favorites, recent playback tracking, and notification support."
    ),
    version="1.0.0",
    contact={
        "name": "Atlas Music Support",
        "email": "support@atlasmusic.com",
        "url": "https://atlasmusic.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {"name": "Health", "description": "Health and readiness checks."},
        {"name": "Auth", "description": "Authentication and account management."},
        {"name": "Users", "description": "Profile and account-related operations."},
        {"name": "Songs", "description": "Song upload, fetch, and management endpoints."},
        {"name": "Favorites", "description": "Favorite song operations."},
        {"name": "Recently Played", "description": "Recent listening history endpoints."},
        {"name": "Notifications", "description": "Push notification delivery endpoints."},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(",") if settings.ALLOWED_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [{"field": e["loc"][-1], "message": e["msg"]} for e in exc.errors()]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": errors},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An unexpected error occurred. Please try again later."
        },
    )


app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["Health"])
def root():
    return {
        "status": "healthy",
        "app": "Atlas Music API",
        "version": "1.0.0",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
