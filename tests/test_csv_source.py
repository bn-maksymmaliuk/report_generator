import pytest

from infrastructure.sources.csv_source import CsvSource


async def test_parses_and_normalizes(tmp_path):
    csv_file = tmp_path / "employees.csv"
    csv_file.write_text(
        "ID,Name,Age,Job,Salary\n"
        "1, Ivan , 30, Engineer, 5000\n"
        "2,Olena,28,Biologist,4000\n",
        encoding="utf-8",
    )

    rows = await CsvSource(str(csv_file)).fetch()

    assert rows == [
        {"id": "1", "name": "Ivan", "age": "30", "job": "Engineer", "salary": "5000"},
        {"id": "2", "name": "Olena", "age": "28", "job": "Biologist", "salary": "4000"},
    ]


async def test_missing_file_raises(tmp_path):
    source = CsvSource(str(tmp_path / "nope.csv"))
    with pytest.raises(FileNotFoundError):
        await source.fetch()


async def test_missing_field_raises(tmp_path):
    csv_file = tmp_path / "bad.csv"
    csv_file.write_text("ID,Name,Age,Job\n1,Ivan,30,Engineer\n", encoding="utf-8")

    with pytest.raises(ValueError, match="salary"):
        await CsvSource(str(csv_file)).fetch()
