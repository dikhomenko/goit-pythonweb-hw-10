from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.routers.auth import schemas
from db.database import get_db
from app.services.auth.jwt_manager import Hash
from app.services.user.user_service import UserService
from app.helpers.email_sender.email import send_email
from app.routers.auth.schemas import UserResponse
from app.services.auth.jwt_manager import JWTManager

hash_handler = Hash()

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register_user(
    body: schemas.UserModel,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
    user_service: UserService = Depends(UserService),
):
    jwt_manager = JWTManager()

    # Check if the email is already registered
    email_user = user_service.get_user_by_email(db, body.email)
    if email_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    # Check if the username is already taken
    username_user = user_service.get_user_by_username(db, body.username)
    if username_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username already exists",
        )

    # Create a new user
    new_user = user_service.create_user(
        db,
        username=body.username,
        hashed_password=hash_handler.get_password_hash(body.password),
        email=body.email,
    )

    # Send confirmation email
    background_tasks.add_task(
        send_email, new_user.email, new_user.username, request.base_url, jwt_manager
    )
    return new_user


@router.post(
    "/login", response_model=schemas.TokenModel, status_code=status.HTTP_200_OK
)
def login(
    body: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    user_service: UserService = Depends(UserService),
    jwt_manager: JWTManager = Depends(JWTManager),
):
    # Fetch the user by username
    user = user_service.get_user_by_username(db, body.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username"
        )

    # Verify the password
    if not hash_handler.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )

    # Check if the email is confirmed
    if not user.confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not confirmed",
        )

    # Generate JWT
    access_token = jwt_manager.create_access_token(data={"sub": user.username})
    return schemas.TokenModel(access_token=access_token, token_type="bearer")
