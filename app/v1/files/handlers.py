from typing import List
from uuid import UUID

from fastapi import File, UploadFile, APIRouter, Form, Depends
from pydantic import Field
from starlette.responses import JSONResponse, FileResponse

from app.v1.files.dependencies import FileDependencyMarker
from app.v1.files.crud import FileRepository
from app.v1.files.schemas import GetFileModel, PostFormModel
from app.v1.files.services import FileService

files_router = APIRouter()


@files_router.post("/files")
async def create_upload_file(
        data: PostFormModel = Depends(),
        db: FileRepository = Depends(FileDependencyMarker),
        file_service: FileService = Depends(),
):
    file_expire_time = file_service.generate_delete_file_date(hours=data.ttl)
    upload_file = await db.create_upload_file(upload_file=data.file, expire_time=file_expire_time)

    data = {"detail": "File created", "uuid": str(upload_file.uuid)}
    return JSONResponse(status_code=201, content=data)


@files_router.get("/files/{file_uuid}/info", response_model=GetFileModel)
async def get_file_info(
        file_uuid: UUID = Field(alias="uuid"),
        db: FileRepository = Depends(FileDependencyMarker),
        file_service: FileService = Depends(),
):
    result = await db.get_upload_file(uuid=file_uuid)
    return file_service.generate_response_model(
        uuid=result.uuid,
        original_name=result.original_name,
        size_bytes=result.size_bytes,
        deleted_at=result.deleted_at,
        status=result.status,
        created_at=result.created_at,
        mime_type=result.mime_type,
    )


@files_router.get("/files", response_model=List[GetFileModel])
async def get_files_info(
        db: FileRepository = Depends(FileDependencyMarker),
        file_service: FileService = Depends(),
):
    result = await db.get_upload_files()
    return [
        file_service.generate_response_model(
            uuid=element.uuid,
            original_name=element.original_name,
            size_bytes=element.size_bytes,
            deleted_at=element.deleted_at,
            status=element.status,
            created_at=element.created_at,
            mime_type=element.mime_type,
        ) for element in result
    ]


@files_router.get("/files/{file_uuid}")
async def get_file(
        file_uuid: UUID = Field(alias="uuid"),
        db: FileRepository = Depends(FileDependencyMarker),
        file_service: FileService = Depends(),
):
    file_db = await db.get_upload_file(uuid=file_uuid)
    file_path = file_service.file_path_from_security_name(file_db.security_name)
    return FileResponse(path=file_path, filename=file_db.original_name)
