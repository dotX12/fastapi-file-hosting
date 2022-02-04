import datetime
import os
from typing import Union
from uuid import UUID

from app.v1.files.schemas import GetFileModel, MetaModel, URLModel, SizeModel


class FileService:

    @staticmethod
    def generate_delete_file_date(hours: int):
        return datetime.datetime.now() + datetime.timedelta(hours=hours)

    @staticmethod
    def file_path_from_security_name(name: str):
        return os.path.join(os.getcwd(), 'files', name)

    @staticmethod
    def generate_response_model(
        uuid: UUID,
        original_name: str,
        size_bytes: Union[int, float],
        mime_type: str,
        deleted_at: datetime,
        created_at: datetime,
        status: bool,
    ):
        url = URLModel(minimal=str(uuid))
        size = SizeModel(bytes=size_bytes)
        meta = MetaModel(name=original_name, mimetype=mime_type, size=size)

        return GetFileModel(
            uuid=uuid,
            created_at=created_at,
            deleted_at=deleted_at,
            available=status,
            meta=meta,
            url=url,
        )
