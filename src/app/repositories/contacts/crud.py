from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select, extract
from db.models.contact import Contact, Email, Phone, AdditionalData
from app.routers.contacts.schemas import ContactCreate, AdditionalDataCreate
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy import func


class ContactsRepository:
    def create_contact(
        self, db: Session, contact: ContactCreate, user_id: int
    ) -> Contact:
        # Convert Pydantic ContactCreate to SQLAlchemy Contact
        db_contact = Contact(
            first_name=contact.first_name,
            last_name=contact.last_name,
            birthday=contact.birthday,
            user_id=user_id,  # Associate the contact with the authenticated user
            emails=[Email(email=email.email) for email in contact.emails],
            phones=[Phone(phone=phone.phone) for phone in contact.phones],
            additional_data=[
                AdditionalData(key=data.key, value=data.value)
                for data in contact.additional_data
            ],
        )
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return db_contact

    def get_contacts(
        self, db: Session, user_id: int, skip: int = 0, limit: int = 10
    ) -> List[Contact]:
        # Retrieve all contacts for the given user
        return (
            db.query(Contact)
            .filter(Contact.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_contact(
        self, db: Session, contact_id: int, user_id: int
    ) -> Optional[Contact]:
        # Retrieve a specific contact by ID for the given user
        return (
            db.query(Contact)
            .filter(Contact.id == contact_id, Contact.user_id == user_id)
            .first()
        )

    def update_contact(
        self, db: Session, contact_id: int, contact: ContactCreate, user_id: int
    ) -> Optional[Contact]:
        db_contact = (
            db.query(Contact)
            .filter(Contact.id == contact_id, Contact.user_id == user_id)
            .first()
        )
        if db_contact:

            for key, value in contact.model_dump(exclude_unset=True).items():
                if key not in ["emails", "phones", "additional_data"]:
                    setattr(db_contact, key, value)

            # Replace emails
            if contact.emails:
                db_contact.emails.clear()  # Clear existing emails
                db.commit()  # Commit to ensure old emails are deleted
                db_contact.emails.extend(
                    [Email(email=email.email) for email in contact.emails]
                )

            # Replace phones
            if contact.phones:
                db_contact.phones.clear()  # Clear existing phones
                db.commit()  # Commit to ensure old phones are deleted
                db_contact.phones.extend(
                    [Phone(phone=phone.phone) for phone in contact.phones]
                )

            # Replace additional_data
            if contact.additional_data:
                db_contact.additional_data.clear()  # Clear existing additional_data
                db.commit()  # Commit to ensure old additional_data is deleted
                db_contact.additional_data.extend(
                    [
                        AdditionalData(key=data.key, value=data.value)
                        for data in contact.additional_data
                    ]
                )

            db.commit()
            db.refresh(db_contact)
        return db_contact

    def delete_contact(
        self, db: Session, contact_id: int, user_id: int
    ) -> Optional[Contact]:
        db_contact = (
            db.query(Contact)
            .filter(Contact.id == contact_id, Contact.user_id == user_id)
            .first()
        )
        if db_contact:
            db.delete(db_contact)
            db.commit()
        return db_contact

    def get_contact_by_name_lastname_email(
        self,
        db: Session,
        user_id: int,
        name: Optional[str] = None,
        lastname: Optional[str] = None,
        email: Optional[str] = None,
    ) -> List[Contact]:
        query = db.query(Contact).filter(Contact.user_id == user_id)
        if name:
            query = query.filter(func.lower(Contact.first_name) == name.lower())
        if lastname:
            query = query.filter(func.lower(Contact.last_name) == lastname.lower())
        if email:
            query = query.join(Contact.emails).filter(
                func.lower(Email.email) == email.lower()
            )
        return query.all()

    def get_contacts_with_upcoming_birthdays(
        self, db: Session, user_id: int
    ) -> List[Contact]:
        today = datetime.today()
        next_week = today + timedelta(days=7)

        today_month = today.month
        today_day = today.day
        next_week_month = next_week.month
        next_week_day = next_week.day

        if today_month == next_week_month:
            # If the range is within the same month
            res = self._get_birthdays_same_month(
                db, user_id, today_month, today_day, next_week_day
            )
        else:
            # If the range is e.g. March 30 to April 5
            res = self._get_birthdays_months_overlap(
                db, user_id, today_month, today_day, next_week_month, next_week_day
            )
        return res

    def _get_birthdays_same_month(
        self,
        db: Session,
        user_id: int,
        today_month: int,
        today_day: int,
        next_week_day: int,
    ) -> List[Contact]:
        return (
            db.query(Contact)
            .filter(
                Contact.user_id == user_id,
                extract("month", Contact.birthday) == today_month,
                extract("day", Contact.birthday).between(today_day, next_week_day),
            )
            .all()
        )

    def _get_birthdays_months_overlap(
        self,
        db: Session,
        user_id: int,
        today_month: int,
        today_day: int,
        next_week_month: int,
        next_week_day: int,
    ) -> List[Contact]:
        return (
            db.query(Contact)
            .filter(
                Contact.user_id == user_id,
                (extract("month", Contact.birthday) == today_month)
                & (extract("day", Contact.birthday) >= today_day)
                | (extract("month", Contact.birthday) == next_week_month)
                & (extract("day", Contact.birthday) <= next_week_day),
            )
            .all()
        )
