from pydantic import BaseModel
from datetime import datetime


class ContextBase(BaseModel):
    context_text: str
    model: str
    role: str

class ContextCreate(ContextBase):
    pass


class Context(ContextBase):
    created_at: datetime
    context_id: int 

    class Config:
        from_attributes = True
