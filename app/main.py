import json
import cloudinary
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from app.core.base import Base
from app.db.session import engine
from app.api.v1.api import api_router
from app.middleware.cloudinary_middleware import configure_cloudinary
from firebase_admin import credentials
import firebase_admin
from app.core.config import settings


# ── Lifespan — startup / shutdown ────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    configure_cloudinary()
    cred = credentials.Certificate(json.loads(settings.FIREBASE_CREDENTIALS))
    firebase_admin.initialize_app(cred)
    print("🚀 Atlas Music API is live")
    yield
    # shutdown
    print("🛑 Atlas Music API shutting down")


app = FastAPI(
    lifespan=lifespan,
    
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
    
    title="🎵 ATLAS MUSIC API",
    summary="A modern music streaming backend built with FastAPI that serves as the backend for managing music metadata, user authentication, and streaming services. This API provides endpoints for tracks, albums, artists, and playlists, supporting a full-featured music application experience",
    description="""
## Welcome to the Atlas Music API 🎶

Built with **FastAPI** · Powered by **PostgreSQL** · Stored on **Cloudinary**

---

### 🔐 Authentication
All protected endpoints require an `x-auth-token` header containing a valid JWT.
Supports both **email/password** and **Google Sign-In**.

---

#  📦 Core Features

🎵 Songs | Upload, stream, and manage songs |
👤 Users | Register, login, update profile |
❤️Favorites | Toggle and fetch favorite songs |
🕐 Recently Played | Auto-tracked listening history |
🔔 Notifications | Firebase push notifications |
☁️ File Storage | Cloudinary for audio and thumbnails |

---

1. Register at `POST /api/v1/auth/signup`
2. Login at `POST /api/v1/auth/signin` or `POST /api/v1/auth/google`
3. Use the returned token in the `x-auth-token` header
4. Explore the endpoints below
    """,
    version="1.0.0",
    
    contact={
        "name": "Little Tech Support",
        "email": "support@atlasmusic.com",
        "url": "https://atlasmusic.com",
    },
    
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    
    openapi_tags=[
        {
            "name": "Health",
            "description": "API health check endpoints.",
        },
        {
            "name": "Auth",
            "description": "User registration, login, Google Sign-In, and profile.",
        },
        {
            "name": "Songs",
            "description": "Upload, fetch, and manage songs.",
        },
        {
            "name": "Favorites",
            "description": "Toggle and retrieve favorite songs.",
        },
        {
            "name": "Recently Played",
            "description": "Fetch and update listening history.",
        },
        {
            "name": "Notifications",
            "description": "Firebase push notification registration.",
        },
    ],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
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
        content={"detail": "An unexpected error occurred. Please try again."},
    )

app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Health"])
def root():
    return {
        "status": "healthy",
        "app": "Atlas Music API",
        "version": "1.0.0",
    }

app = FastAPI(
    docs_url="/api/v1/docs",
    
    title="ATLAS MUSIC API",
    description="A comprehensive Music Streaming API that serves as the backend for managing music metadata, user authentication, and streaming services. This API provides endpoints for tracks, albums, artists, and playlists, supporting a full-featured music application experience.",
    version="1.0.0",
)
