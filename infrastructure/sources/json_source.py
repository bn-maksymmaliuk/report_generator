import json
import logging
from pathlib import Path

import aiofiles

from domain.sources.base import BaseSource
from domain.types import Employee

logger = logging.getLogger(__name__)


class JsonSource(BaseSource):
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    async def fetch(self) -> list[Employee]:
        if not self.file_path.is_file():
            raise FileNotFoundError(f"JSON source not found: {self.file_path}")

        logger.info(f"Reading JSON from {self.file_path}")

        async with aiofiles.open(self.file_path, mode="r", encoding="utf-8") as file:
            content = await file.read()

        rows = json.loads(content)
        if not isinstance(rows, list):
            raise ValueError("JSON source must contain a top-level array")

        return [self.normalize_row(row) for row in rows]
