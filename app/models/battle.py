from datetime import date

from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.db import Base


class Battle(Base):
    __tablename__ = 'battles'
    id: Mapped[int] = mapped_column(primary_key=True)
    for_user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)
    hour: Mapped[int]
    date: Mapped[date]

    for_user: Mapped["User"] = relationship(back_populates="reminders")
    __table_args__ = (
        UniqueConstraint('hour', 'date'),
    )
