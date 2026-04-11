from shared.types import Employee
from sources.base import BaseSource
import csv

class CsvSource(BaseSource):
    def __init__(self, file_path: str):
        self.file_path = file_path

    async def fetch(self) -> list[Employee]:
        with open(self.file_path, mode="r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)

            return [self.normalize_row(row) for row in csv_reader]
