from pydantic import BaseModel, ConfigDict
from typing import Optional

class TokenBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class Token(TokenBase):
    access_token: str
    token_type: str

class TokenData(TokenBase):
    id: Optional[int] = None