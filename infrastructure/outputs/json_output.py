import json
import logging
from datetime import datetime
from pathlib import Path

import aiofiles

from domain.outputs.base import BaseOutput

logger = logging.getLogger(__name__)


class JsonOutput(BaseOutput):
    def __init__(self, output_dir: str, file_prefix: str = "report"):
        self.output_dir = Path(output_dir)
        self.file_prefix = file_prefix

    async def write(self, data: list[dict]) -> str:
        self.output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        file_path = self.output_dir / f"{self.file_prefix}-{timestamp}.json"

        payload = json.dumps(data, indent=4, ensure_ascii=False)
        async with aiofiles.open(file_path, mode="w", encoding="utf-8") as file:
            await file.write(payload)

        logger.info(f"Wrote {len(data)} rows to {file_path}")
        return str(file_path)
