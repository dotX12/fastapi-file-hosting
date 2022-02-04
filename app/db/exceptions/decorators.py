from typing import Optional

from sqlalchemy.exc import NoResultFound

from app.handlers.models import ExceptionSQL


def handle_not_found_error(_: Optional[NoResultFound] = None, __: Optional[str] = None):
    raise ExceptionSQL(
        detail="Запись, которую вы ищите или удаляете, отсутствует в базе данных"
    )


def orm_error_handler(func):
    async def decorator(*args, **kwargs):
        try:
            return await func(*args, **kwargs)

        except NoResultFound:
            handle_not_found_error()

    return decorator
