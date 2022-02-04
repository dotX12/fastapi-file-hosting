from datetime import datetime
from typing import Type, Any, Dict, Optional
from uuid import UUID

from pydantic import validator

from app.schemas.base import BaseModelORM
from app.v1.files.utils import convert_size
from config import settings_app


class URLModel(BaseModelORM):
    minimal: str

    @validator("minimal", always=True)
    def validate_minimal(cls: Type['URLModel'], v: Any) -> str:
        return f"{settings_app.HOSTING_URL}/files/{v}"


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


responses = {
    200: {
        "model": GetFileModel,
        "description": "Good request"
    }

}
