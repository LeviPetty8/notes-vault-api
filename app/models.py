import uuid
from datetime import datetime as date, timezone as zone
from sqlalchemy import String, Text, DateTime as Date
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Note(Base):
    __tablename__ = "notes"

    id: Mapped[str] = mapped_column(String, primary_key = True, default = lambda: str(uuid.uuid4()))
    title: Mapped[str | None] = mapped_column(String(200), nullable = True)
    content: Mapped[str] = mapped_column(Text, nullable = False)
    created_at: Mapped[date] = mapped_column(
        Date(zone=True),
        default = lambda: date.now(zone.utc)
    )