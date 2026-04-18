import json
from pathlib import Path

from infrastructure.outputs.json_output import JsonOutput


async def test_writes_file_and_creates_dir(tmp_path):
    target = tmp_path / "nested" / "results"
    output = JsonOutput(str(target), file_prefix="employee")

    data = [{"Name": "Ivan", "Job": "Engineer"}]
    path = await output.write(data)

    written = Path(path)
    assert written.exists()
    assert written.parent == target
    assert written.name.startswith("employee-")
    assert json.loads(written.read_text(encoding="utf-8")) == data
