from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.handlers.models import ExceptionSQL


def sql_exception_handler(_: Request, exc: ExceptionSQL):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": exc.detail,
            "sql_detail": exc.sql_detail
        }
    )
