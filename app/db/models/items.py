from ..database import BaseItem
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    Float,
    TIMESTAMP,
    String,
    text,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from .users import User


class Item(BaseItem):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    is_published = Column(Boolean, server_default="TRUE", nullable=False)
    price = Column(Float, server_default="0.00", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("DATETIME('now')")
    )
    owner_id = Column(
        Integer,
        # ForeignKey(column="users.id", ondelete="CASCADE"),
        ForeignKey(column=User.id, ondelete="CASCADE"),
        nullable=False,
    )
    owner = relationship(User)
