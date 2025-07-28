from datetime import datetime

from sqlalchemy import ForeignKey, String, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.database.session import Model
from enum import Enum as PyEnum


class TicketStatus(str, PyEnum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"


class Ticket(Model):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="tickets")

    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[TicketStatus] = mapped_column(Enum(TicketStatus), default=TicketStatus.PENDING)     #add a status list to it
    created_at: Mapped[datetime] = mapped_column(DateTime, default = datetime.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default = datetime.now())


