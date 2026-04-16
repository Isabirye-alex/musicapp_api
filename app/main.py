import cloudinary
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.core.base import Base
from app.db.session import engine
from app.api.v1.api import api_router
from app.services.cloudinary import configure_cloudinary


app = FastAPI(
    title="Music App API",
    description="My API is gonna work as the backend server to my client application",
    version="1.0.0.0",
)
Base.metadata.create_all(bind=engine)
configure_cloudinary()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [{"field": e["loc"][-1], "message": e["msg"]} for e in exc.errors()]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": errors}
    )


app.include_router(api_router, prefix="/api/v1")
