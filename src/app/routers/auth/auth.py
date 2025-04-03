from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.routers.auth import schemas
from db.database import get_db
from app.helpers.auth.jwt_manager import create_access_token, get_current_user, Hash
from db.models.user import User
from app.repositories.users.users import (
    get_user_by_username,
    get_user_by_email,
    create_user,
)  # Import repository functions
from app.helpers.email_sender.email import send_email
from app.routers.auth.schemas import UserResponse

hash_handler = Hash()

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


# @router.post("/signup", status_code=status.HTTP_201_CREATED)
# def signup(body: schemas.UserModel, db: Session = Depends(get_db)):
#     # Check if the username is already taken
#     exist_user = get_user_by_username(db, body.username)
#     if exist_user:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT, detail="Username is already taken"
#         )

#     # Check if the email is already taken
#     exist_user_by_email = get_user_by_email(db, body.email)
#     if exist_user_by_email:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT, detail="Email is already taken"
#         )

#     # Create a new user
#     new_user = create_user(
#         db,
#         username=body.username,
#         hashed_password=hash_handler.get_password_hash(body.password),
#         email=body.email,
#     )
#     return {"new_user": new_user.username}


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register_user(
    body: schemas.UserModel,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    email_user = get_user_by_email(db, body.email)
    if email_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    username_user = get_user_by_username(db, body.username)
    if username_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username already exists",
        )
    new_user = create_user(
        db,
        username=body.username,
        hashed_password=hash_handler.get_password_hash(body.password),
        email=body.email,
    )

    background_tasks.add_task(
        send_email, new_user.email, new_user.username, request.base_url
    )
    return new_user


@router.post(
    "/login", response_model=schemas.TokenModel, status_code=status.HTTP_200_OK
)
def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Fetch the user by username
    user = get_user_by_username(db, body.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username"
        )

    # Verify the password
    if not hash_handler.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )

    if not user.confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not confirmed",
        )
    # Generate JWT
    access_token = create_access_token(data={"sub": user.username})
    return schemas.TokenModel(access_token=access_token, token_type="bearer")
