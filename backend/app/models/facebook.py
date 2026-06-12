import uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Uuid, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class FacebookPage(Base):
    __tablename__ = "facebook_pages"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    page_id: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    page_name: Mapped[str] = mapped_column(String, nullable=False)
    access_token_encrypted: Mapped[str] = mapped_column(Text, nullable=False)
    token_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    connected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

