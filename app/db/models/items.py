from ..database import BaseItem
from sqlalchemy import Boolean, Column, Float, Integer, TIMESTAMP, String, text

class User(BaseItem):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, nullable=False)
    desc = Column(String, nullable=False)
    draft = Column(Boolean, nullable=False, server_default="FALSE")
    price = Column(Float, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )