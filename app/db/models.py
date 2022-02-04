from sqlalchemy import Column, String, Numeric, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.functions import current_timestamp

from misc import Base


class TimestampMixin(object):
    created_at = Column(DateTime, default=current_timestamp())
    updated_at = Column(DateTime, onupdate=current_timestamp())


class UploadFile(TimestampMixin, Base):
    __tablename__ = "files"

    uuid = Column(UUID(as_uuid=True), primary_key=True)
    original_name = Column(String(255))
    security_name = Column(String(255))
    size_bytes = Column(Numeric)
    mime_type = Column(String(255))
    deleted_at = Column(DateTime)
