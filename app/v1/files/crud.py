from datetime import datetime
from typing import List
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud import BaseCRUD
from app.db.exceptions.decorators import orm_error_handler
from app.db.models import FileModel
from app.v1.files.utils import UploadFileHelper


class FileRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.model = FileModel

        self.base = BaseCRUD(db_session=db_session, model=self.model)

    async def create_upload_file(self, upload_file: UploadFile, expire_time: datetime) -> FileModel:
        ufh = UploadFileHelper(upload_file)
        await ufh.save_file()

        async with self.base.transaction():
            return await self.base.insert(
                uuid=ufh.uuid,
                original_name=ufh.original_filename,
                security_name=ufh.security_filename,
                size_bytes=ufh.size,
                mime_type=ufh.content_type,
                deleted_at=expire_time,
            )

    @orm_error_handler
    async def get_upload_file(self, uuid: UUID) -> FileModel:
        async with self.base.transaction():
            return await self.base.get_one(self.model.uuid == uuid)

    @orm_error_handler
    async def get_upload_files(self) -> List[FileModel]:
        async with self.base.transaction():
            return await self.base.get_many()
