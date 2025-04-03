from sqlalchemy.orm import Session
from db.models.user import User


def get_user_by_username(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, id: int) -> User:
    return db.query(User).filter(User.id == id).first()


def create_user(db: Session, username: str, hashed_password: str, email: str) -> User:
    new_user = User(username=username, password=hashed_password, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def confirmed_email(db: Session, email: str) -> None:
    user = get_user_by_email(db, email)
    user.confirmed = True
    db.commit()
