from pydantic import BaseModel
from datetime import datetime

from pydantic import BaseModel
from datetime import datetime

class TokenBase(BaseModel):
    token_name: str

class TokenCreate(TokenBase):
    pass

class TokenResponse(TokenBase):
    id: int
    created_at: datetime
    partial_token: str
    token_name: str
    
    class Config:
        from_attributes = True