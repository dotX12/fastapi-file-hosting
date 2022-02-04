import math
import os
from uuid import uuid4
from aiofile import Writer, AIOFile

from fastapi import UploadFile


class UploadFileHelper:
    def __init__(self, file: UploadFile):
        self.file = file
        self._uuid = uuid4()

    @property
    def uuid(self):
        return self._uuid

    @property
    def security_filename(self):
        return f'{str(self._uuid)}__{self.file.filename}'

    @property
    def original_filename(self):
        return self.file.filename

    @property
    def content_type(self):
        return self.file.content_type

    @property
    def size(self):
        return len(self.open_file)

    async def _open(self):
        self.open_file = await self.file.read()

    async def _close(self):
        await self.file.close()

    async def save_file(self):
        await self._open()

        path_file = os.path.join(os.getcwd(), 'files', self.security_filename)
        async with AIOFile(path_file, 'wb') as buffer:
            writer = Writer(buffer)
            await writer(self.open_file)

        await self._close()


def convert_size(size_bytes: int):
    if size_bytes == 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"
