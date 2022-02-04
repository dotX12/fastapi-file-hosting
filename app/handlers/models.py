from typing import Optional


class ExceptionSQL(Exception):
    def __init__(self, detail: str, sql_detail: Optional[str] = None):
        self.detail = detail
        self.sql_detail = sql_detail
