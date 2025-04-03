from db.models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, Integer, String, Boolean, func


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    avatar = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())
    confirmed = Column(Boolean, default=False)

    # Relationship with Contact
    contacts = relationship(
        "Contact", back_populates="user", cascade="all, delete-orphan"
    )
