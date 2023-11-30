from datetime import datetime

from sqlalchemy import Integer, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    name: Mapped[str]
    username: Mapped[str] = mapped_column(String(32), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(nullable=True)

    reminders: Mapped[list["Battle"]] = relationship(back_populates="for_user")
