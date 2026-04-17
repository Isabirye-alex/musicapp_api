from fastapi import APIRouter
from app.api.v1.endpoints.auth.sign_up import router as signup_router
from app.api.v1.endpoints.auth.login import router as login_router
from app.api.v1.endpoints.auth.fetch_users import router as users_router
from app.api.v1.endpoints.songs.song import router as song_router

api_router = APIRouter()
api_router.include_router(signup_router, prefix="/auth", tags=["auth"])
api_router.include_router(login_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/auth", tags=["auth"])
api_router.include_router(song_router, prefix="/songs", tags=['songs'])
