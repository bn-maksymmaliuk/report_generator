import json
from datetime import datetime
from app.outputs.base import BaseOutput
import logging

logger = logging.getLogger(__name__)

class JsonOutput(BaseOutput):
    def __init__(self, output: str):
        self.output = output

    async def write(self, data: list[dict]) -> str:

        try:
            logger.info(f"Writing data to {len(data)} employees.")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = f"{self.output}/employees-{timestamp}.json"

            with open(file_path, mode="w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            return file_path
        except FileNotFoundError:
            logger.error(f"Dir {self.output} not found.")
            raise
