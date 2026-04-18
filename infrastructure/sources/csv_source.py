import csv
import io
import logging
from pathlib import Path

import aiofiles

from domain.sources.base import BaseSource
from domain.types import Employee

logger = logging.getLogger(__name__)


class CsvSource(BaseSource):
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    async def fetch(self) -> list[Employee]:
        if not self.file_path.is_file():
            raise FileNotFoundError(f"CSV source not found: {self.file_path}")

        logger.info(f"Reading CSV from {self.file_path}")

        async with aiofiles.open(self.file_path, mode="r", encoding="utf-8") as file:
            content = await file.read()

        reader = csv.DictReader(io.StringIO(content))
        return [self.normalize_row(row) for row in reader]
