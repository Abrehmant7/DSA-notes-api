from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(
        String(200),
        index=True,
    )
    signal: Mapped[str] = mapped_column(Text)
    brute_force: Mapped[str] = mapped_column(Text)
    useful_memory: Mapped[str] = mapped_column(Text)
    pattern: Mapped[str] = mapped_column(
        String(100),
        index=True,
    )
    key_question: Mapped[str] = mapped_column(Text)
    solution_approach: Mapped[str] = mapped_column(Text)
    time_complexity: Mapped[str] = mapped_column(Text)
    space_complexity: Mapped[str] = mapped_column(Text)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        index=True,
    )

    category: Mapped["Category"] = relationship(
        back_populates="notes"
    )
