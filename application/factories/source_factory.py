from domain.sources.base import BaseSource
from infrastructure.sources.csv_source import CsvSource
from schemas.schemas import SourceType


SOURCE_TYPES_MAP: dict[SourceType, type] = {
    SourceType.CSV: CsvSource,
}

class SourceFactory:
    @staticmethod
    def create(source_type: SourceType, source_path: str) -> BaseSource:
        source_cls = SOURCE_TYPES_MAP.get(source_type)

        if not source_cls:
            raise ValueError(
                f"Unsupported source type: {source_type}. "
                f"Available: {[t.value for t in SOURCE_TYPES_MAP]}"
            )

        return source_cls(source_path)