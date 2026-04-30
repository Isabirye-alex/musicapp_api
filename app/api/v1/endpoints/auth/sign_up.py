from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.user.user_signup_crud import create_user
from app.db.session import get_db
from app.schemas.user_schema import UserCreate
from app.services.fetch_use_by_email import get_user_by_email
from app.services.email_service import send_registration_email

router = APIRouter()

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def sign_up(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    # Check if user exists
    existing = get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    try:
        new_user = create_user(db, user)
        print("Sending Email........")
        background_tasks.add_task(
            send_registration_email,
            new_user.email,
            new_user.first_name,
            new_user.last_name,
        )
        print("Email Sent........")

        return {"status": "success", "message": "User created successfully"}

    except Exception as e:
        # Proper server error handling
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
