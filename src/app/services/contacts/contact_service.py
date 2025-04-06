from sqlalchemy.orm import Session
from app.repositories.contacts.crud import ContactsRepository
from fastapi import Depends
from typing import List, Optional
from db.models.contact import Contact


class ContactService:
    def __init__(self, contacts_repository: ContactsRepository = Depends()):
        self.contacts_repository = contacts_repository

    def get_contact(self, db: Session, contact_id: int, user_id: int) -> Contact:
        return self.contacts_repository.get_contact(db, contact_id, user_id)

    def get_contacts(
        self, db: Session, user_id: int, skip: int = 0, limit: int = 10
    ) -> List[Contact]:
        return self.contacts_repository.get_contacts(db, user_id, skip, limit)

    def create_contact(self, db: Session, contact_data: dict, user_id: int) -> Contact:
        return self.contacts_repository.create_contact(db, contact_data, user_id)

    def update_contact(
        self, db: Session, contact_id: int, contact_data: dict, user_id: int
    ) -> Optional[Contact]:
        return self.contacts_repository.update_contact(
            db, contact_id, contact_data, user_id
        )

    def delete_contact(
        self, db: Session, contact_id: int, user_id: int
    ) -> Optional[Contact]:
        return self.contacts_repository.delete_contact(db, contact_id, user_id)

    def get_contact_by_name_lastname_email(
        self,
        db: Session,
        user_id: int,
        name: Optional[str],
        lastname: Optional[str],
        email: Optional[str],
    ) -> List[Contact]:
        return self.contacts_repository.get_contact_by_name_lastname_email(
            db, user_id, name, lastname, email
        )

    def get_contacts_with_upcoming_birthdays(
        self, db: Session, user_id: int
    ) -> List[Contact]:
        return self.contacts_repository.get_contacts_with_upcoming_birthdays(
            db, user_id
        )
