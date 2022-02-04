from datetime import datetime
from typing import Type, Any, Dict, Optional
from uuid import UUID

from fastapi import UploadFile, File, Form
from pydantic import validator

from app.schemas.base import BaseModelORM
from app.v1.files.misc import UPLOAD_FILE_TTL_DESCRIPTION
from app.v1.files.utils import convert_size
from config import settings_app


class PostFormModel:
    def __init__(
        self,
        file: UploadFile = File(..., description="File to upload."),
        ttl: int = Form(default=1, ge=1, le=180, description=UPLOAD_FILE_TTL_DESCRIPTION)
    ):
        self.file = file
        self.ttl = ttl


class URLModel(BaseModelORM):
    minimal: str

    @validator("minimal", always=True)
    def validate_minimal(cls: Type['URLModel'], v: Any) -> str:
        try:
            assert UUID(v)
            return f"{settings_app.HOSTING_URL}/files/{v}"
        except ValueError:
            return v


class SizeModel(BaseModelORM):
    bytes: int
    readable: Optional[str] = None

    @validator("readable", always=True)
    def validate_readable(cls: Type['SizeModel'], _: Any, values: Dict[str, Any]) -> str:
        _bytes = values.get("bytes")
        return convert_size(_bytes)


class MetaModel(BaseModelORM):
    name: str
    mimetype: str
    size: SizeModel


class GetFileModel(BaseModelORM):
    uuid: UUID
    url: URLModel
    meta: MetaModel
    created_at: datetime
    deleted_at: datetime
    available: bool

