import pytest
from datetime import date
from unittest.mock import patch

from employee_tracker.domain.tracker import Tracker
from employee_tracker.domain.employee import Employee

def test_tracker_created_successfully():
    trk = Tracker()
    assert hasattr(trk,"employees")
    assert hasattr(trk,"departments")
    assert hasattr(trk,"permissions")
@patch("employee_tracker.domain.tracker.Employee")
def test_create_employee_calls_employee_constructor(mock_employee):
    trk = Tracker()
    trk.create_employee("John","Boss",date(2024, 10, 2),50000,"My Address")
    mock_employee.assert_called_once_with(
        "John",
        "Boss",
        date(2024, 10, 2),
        50000,
        "My Address",
        None,
    )
def test_create_employee_adds_to_employees():
    trk = Tracker()
    id = trk.create_employee("John","Boss",date(2024, 10, 2),50000,"My Address")
    assert len(trk.employees) == 1
    assert trk.employees[id.id].name == "John"

    
