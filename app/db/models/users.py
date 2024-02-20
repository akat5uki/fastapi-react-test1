from ..database import BaseUser
from sqlalchemy import Column, Integer, String, TIMESTAMP, text

class User(BaseUser):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("DATETIME('now')")
    )
    phone_number = Column(String)
