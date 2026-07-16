from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# SQLAlchemy uses declarative mapping through a base class, mapped classes, Mapped type annotations and mapped_column(). The relationship() construct connects ORM classes, while ForeignKey() creates the database-level relationship between columns. dono alag h


# SQLAlchemy uses Base to collect information about every table.
# Every SQLAlchemy model inherits from this class.
class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
    )

    notes: Mapped[list["Note"]] = relationship(
        back_populates="category"
    )


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

