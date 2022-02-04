from fastapi import APIRouter

from app.v1.files.handlers import files_router

own_router_v1 = APIRouter()
own_router_v1.include_router(files_router, tags=['Files'])
