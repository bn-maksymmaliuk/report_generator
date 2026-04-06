from enum import Enum

from pydantic import BaseModel

class SourceType(str, Enum):
    CSV = "csv"
    JSON = "json"
    API = "api"
    DATABASE = "database"

class OutputType(str, Enum):
    CSV = "csv"
    JSON = "json"

class ReportRequest(BaseModel):
    source_path: str
    source_type: SourceType
    output_type: OutputType
    output_dir: str