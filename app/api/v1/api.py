from fastapi import APIRouter
from app.api.v1.endpoints.auth.sign_up import router as signup_router

api_router = APIRouter()
api_router.include_router(signup_router, prefix="/auth", tags=["auth"])
