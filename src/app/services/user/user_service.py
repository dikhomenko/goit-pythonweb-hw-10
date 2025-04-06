from sqlalchemy.orm import Session
from fastapi import Depends
from app.repositories.users.users import UsersRepository


class UserService:
    def __init__(self, users_repository: UsersRepository = Depends()):
        self.users_repository = users_repository

    def get_user_by_username(self, db: Session, username: str):
        return self.users_repository.get_user_by_username(db, username)

    def get_user_by_email(self, db: Session, email: str):
        return self.users_repository.get_user_by_email(db, email)

    def get_user_by_id(self, db: Session, user_id: int):
        return self.users_repository.get_user_by_id(db, user_id)

    def create_user(self, db: Session, username: str, hashed_password: str, email: str):
        return self.users_repository.create_user(db, username, hashed_password, email)

    def confirmed_email(self, db: Session, email: str):
        return self.users_repository.confirmed_email(db, email)

    def update_avatar_url(self, db: Session, email: str, url: str):
        return self.users_repository.update_avatar_url(db, email, url)
