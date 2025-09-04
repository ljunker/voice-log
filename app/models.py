from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text, Integer, DateTime


class Base(DeclarativeBase):
    pass


class LogEntry(Base):
    __tablename__ = "log_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    transcript_raw: Mapped[str] = mapped_column(Text, nullable=False)
    transcript_formal: Mapped[str] = mapped_column(Text, nullable=False)
    duration_sec: Mapped[int] = mapped_column(Integer, nullable=True)

    def __repr__(self) -> str:
        return f"<LogEntry id={self.id} created_at={self.created_at!r} filename={self.filename!r}>"
