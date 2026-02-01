import pytest
from unittest.mock import patch

from employee_tracker.domain.employee import Employee
from employee_tracker.domain.permission import Permission

from datetime import date

def valid_employee_kwargs():
    return dict(
        name="James",
        role="Creator",
        start_date=date(2024, 10, 2),
        salary=30000,
        address="123 Lane, Town, County",
    )
def valid_permission_kwargs():
     return dict(
        name = "per_1",
     )
def valid_department_kwargs():
    return dict(
        name="Finance",
        description = "It's where the money is",
        head_of_department = Employee(**valid_employee_kwargs())
    )


class TestPermissionCreation:
    def test_permission_can_be_created(self):
        per = Permission(**valid_permission_kwargs())
        assert hasattr(per,"name")
        assert hasattr(per,"department")

class TestPermissionTypeValidation:
     @pytest.mark.parametrize(
        "field,value,error",
        [
            ("name", 123, "Name must be a string"),
            ("department", 3.45, "department must be a str"),
        ],
     )
     def test_invalid_datatypes(self, field, value, error):
        kwargs = valid_permission_kwargs()
        kwargs[field] = value

        with pytest.raises(TypeError, match=error):
            Permission(**kwargs)
