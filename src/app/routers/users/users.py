from fastapi import APIRouter, Depends, Request, HTTPException, status, BackgroundTasks
from app.routers.users import schemas
from app.helpers.auth.jwt_manager import get_current_user
from app.helpers.api.rate_limiter import limiter
from app.repositories.users.users import get_user_by_email
from sqlalchemy.orm import Session
from app.repositories.users import users
from app.helpers.auth.jwt_manager import get_email_from_token
from db.database import get_db
from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
from app.settings import settings
from app.routers.users.schemas import RequestEmail, EmailSchema
from app.helpers.email_sender.email import send_email

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS,
)

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/me",
    response_model=schemas.UserResponse,
    description="No more than 5 requests per minute",
)
@limiter.limit("5/minute")
def me(
    request: Request, current_user: schemas.UserResponse = Depends(get_current_user)
):
    return current_user


@router.get("/confirmed_email/{token}")
def confirmed_email(token: str, db: Session = Depends(get_db)):
    email = get_email_from_token(token)
    user = users.get_user_by_email(db, email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error"
        )
    if user.confirmed:
        return {"message": "You have already confirmed your email"}
    users.confirmed_email(db, email)
    return {"message": "Email confirmed successfully"}


@router.post("/request_email")
def request_email(
    body: RequestEmail,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    user = users.get_user_by_email(db, body.email)

    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(
            send_email, user.email, user.username, request.base_url
        )
    return {"message": "Check your email for confirmation"}
