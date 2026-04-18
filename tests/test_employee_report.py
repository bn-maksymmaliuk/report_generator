import pytest

from infrastructure.reports.employee_report import EmployeeReport


def make_row(**overrides):
    row = {"id": "1", "name": "Ivan", "age": "30", "job": "Engineer", "salary": "5000"}
    row.update(overrides)
    return row


async def test_filters_by_min_salary():
    report = EmployeeReport(min_salary=3500)
    data = [
        make_row(id="1", name="Ivan", job="Engineer", salary="5000"),
        make_row(id="2", name="Petro", job="Clerk", salary="2000"),
        make_row(id="3", name="Olena", job="Biologist", salary="3500"),
    ]

    result = await report.process(data)

    assert result == [{"Name": "Ivan", "Job": "Engineer"}]


async def test_extra_fields_are_appended():
    report = EmployeeReport(min_salary=0, extra_fields=["id", "age"])
    result = await report.process([make_row(id="7", age="29")])

    assert result == [{"Name": "Ivan", "Job": "Engineer", "id": "7", "age": "29"}]


async def test_invalid_salary_is_skipped():
    report = EmployeeReport(min_salary=0)
    data = [make_row(salary="abc"), make_row(id="2", name="Ok", salary="100")]

    result = await report.process(data)

    assert result == [{"Name": "Ok", "Job": "Engineer"}]


async def test_mutable_default_is_isolated():
    first = EmployeeReport()
    second = EmployeeReport()
    first.extra_fields.append("id")

    assert second.extra_fields == []
