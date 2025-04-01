from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date


class EmailBase(BaseModel):
    email: EmailStr


class EmailCreate(EmailBase):
    pass


class Email(EmailBase):
    id: int
    contact_id: int

    class Config:
        from_attributes = True


class PhoneBase(BaseModel):
    phone: str


class PhoneCreate(PhoneBase):
    pass


class Phone(PhoneBase):
    id: int
    contact_id: int

    class Config:
        from_attributes = True


class AdditionalDataBase(BaseModel):
    key: str
    value: Optional[str] = None


class AdditionalDataCreate(AdditionalDataBase):
    pass


class AdditionalData(AdditionalDataBase):
    id: int

    class Config:
        from_attributes = True


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    birthday: Optional[date]


class ContactCreate(ContactBase):
    emails: List[EmailCreate] = []
    phones: List[PhoneCreate] = []
    additional_data: List[AdditionalDataCreate] = []


class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birthday: Optional[date] = None
    emails: Optional[List[EmailCreate]] = None
    phones: Optional[List[PhoneCreate]] = None
    additional_data: Optional[List[AdditionalDataCreate]] = None


class Contact(ContactBase):
    id: int
    emails: List[Email] = []
    phones: List[Phone] = []
    additional_data: List[AdditionalData] = []

    class Config:
        from_attributes = True
