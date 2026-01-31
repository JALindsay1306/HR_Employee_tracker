import pytest
from unittest.mock import patch

from employee_tracker.domain.employee import Employee
from employee_tracker.domain.permission import Permission
from employee_tracker.domain.department import Department

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
        admin_id = Employee(**valid_employee_kwargs()).id
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
        assert hasattr(per,"admin_id")
        assert hasattr(per,"departments")

class TestPermissionTypeValidation:
     @pytest.mark.parametrize(
        "field,value,error",
        [
            ("name", 123, "Name must be a string"),
            ("admin_id", "Wrong123", "admin must be an employee"),
            ("departments", "finance", "departments must be a dictionary"),
        ],
     )
     def test_invalid_datatypes(self, field, value, error):
        kwargs = valid_permission_kwargs()
        kwargs[field] = value

        with pytest.raises(TypeError, match=error):
            Permission(**kwargs)
class TestDepartmentsValidation:
    def test_check_id_called(self):
        test = valid_permission_kwargs()
        test["departments"] = [[Department(**valid_department_kwargs()).id,"read"]]
        with patch("employee_tracker.domain.permission.check_id", return_value = True) as mock_check_id:
            per_1 = Permission(**test)
            dep_id = test["departments"][0][0]
            mock_check_id.assert_any_call(dep_id, "dep")
            