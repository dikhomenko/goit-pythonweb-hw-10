from sqlalchemy.orm import Session
from db.models.user import User
from sqlalchemy import func


class UsersRepository:
    def get_user_by_username(self, db: Session, username: str) -> User:
        return (
            db.query(User).filter(func.lower(User.username) == username.lower()).first()
        )

    def get_user_by_email(self, db: Session, email: str) -> User:
        return db.query(User).filter(func.lower(User.email) == email.lower()).first()

    def get_user_by_id(self, db: Session, id: int) -> User:
        return db.query(User).filter(User.id == id).first()

    def create_user(
        self, db: Session, username: str, hashed_password: str, email: str
    ) -> User:
        new_user = User(username=username, password=hashed_password, email=email)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def confirmed_email(self, db: Session, email: str) -> None:
        user = self.get_user_by_email(db, email)
        user.confirmed = True
        db.commit()

    def update_avatar_url(self, db: Session, email: str, url: str) -> User:
        user = self.get_user_by_email(db, email)
        user.avatar = url
        db.commit()
        db.refresh(user)
        return user
