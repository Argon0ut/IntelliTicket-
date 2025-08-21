from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.session import Model
from typing import List
#
# from models.ticket import Ticket


class User(Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    tickets: Mapped[List["Ticket"]] = relationship("Ticket", back_populates="user")