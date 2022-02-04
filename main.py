from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.v1.binding import own_router_v1

app = FastAPI()


def get_application_v1() -> FastAPI:
    application = FastAPI(
        debug=True,
        docs_url=None,
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

    return application
