from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()  # Base class for all models
metadata = Base.metadata  # Metadata object for Alembic


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False, unique=True)
    last_name = Column(String, nullable=False, unique=True)
    birthday = Column(Date, nullable=True, unique=True)

    emails = relationship(
        "Email", back_populates="contact", cascade="all, delete-orphan"
    )
    phones = relationship(
        "Phone", back_populates="contact", cascade="all, delete-orphan"
    )
    additional_data = relationship(
        "AdditionalData", back_populates="contact", cascade="all, delete-orphan"
    )


class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    contact_id = Column(
        Integer,
        ForeignKey("contacts.id", ondelete="CASCADE", onupdate="CASCADE"),
    )

    contact = relationship("Contact", back_populates="emails")


class Phone(Base):
    __tablename__ = "phones"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, unique=True, index=True, nullable=False)
    contact_id = Column(
        Integer,
        ForeignKey("contacts.id", ondelete="CASCADE", onupdate="CASCADE"),
    )

    contact = relationship("Contact", back_populates="phones")


class AdditionalData(Base):
    __tablename__ = "additional_data"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, nullable=False)  # Key for the additional data
    value = Column(Text, nullable=True)  # Value for the additional data
    contact_id = Column(
        Integer,
        ForeignKey("contacts.id", ondelete="CASCADE", onupdate="CASCADE"),
    )

    contact = relationship("Contact", back_populates="additional_data")
