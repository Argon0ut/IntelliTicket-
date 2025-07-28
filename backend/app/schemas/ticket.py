from datetime import datetime

from pydantic import BaseModel
from backend.app.models.ticket import TicketStatus


class UserSchema(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

class CreateTicket(BaseModel):
    user: UserSchema
    title: str
    description: str
    status: str
    created_at: datetime


    class Config:
        orm_mode = True


class ReadTicket(BaseModel):
    id: int
    user: UserSchema
    title: str

class UpdateTicketStatus(BaseModel):
    status: TicketStatus
