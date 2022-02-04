from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.handlers.exceptions import sql_exception_handler
from app.handlers.models import ExceptionSQL
from app.v1.binding import own_router_v1
from app.v1.files import FileRepository, FileDependencyMarker
from misc import async_session


def get_application_v1() -> FastAPI:
    application = FastAPI(
        debug=True,
        title='Files Hosting',
        version='1.2.15',
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=['*']
    )
    application.include_router(own_router_v1)
    application.add_exception_handler(ExceptionSQL, sql_exception_handler)

    application.dependency_overrides.update(
        {
            FileDependencyMarker: lambda: FileRepository(db_session=async_session),
        }
    )

    return application


app = get_application_v1()
