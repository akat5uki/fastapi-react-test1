from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from .users import UserOut


class ItemBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class ItemCreate(ItemBase):
    title: str
    content: str
    is_published: bool = True
    price: float

class Item_s(ItemBase):
    id: int
    title: str
    content: str
    is_published: bool = True
    price: float
    created_at: datetime
    owner_id: int
    owner: UserOut

class ItemOut(ItemBase):
    item: None | Item_s = Field(alias="Item")
    zcount: int