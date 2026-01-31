import pytest
from unittest.mock import patch

from datetime import date
from employee_tracker.domain.department import Department
from employee_tracker.domain.employee import Employee

def valid_employee_kwargs():
    return dict(
        name="James",
        role="Creator",
        start_date=date(2024, 10, 2),
        salary=30000,
        address="123 Lane, Town, County",
    )

def valid_department_kwargs():
    return dict(
        name="Finance",
        description = "It's where the money is",
        head_of_department = Employee(**valid_employee_kwargs())
    )

class TestDepartmentCreation:
    def test_department_can_be_created(self):
        dep = Department(**valid_department_kwargs())
        assert dep.name == "Finance"
        assert dep.description == "It's where the money is"
        assert dep.head_of_department.name == "James"
        assert dep.head_of_department.role == "Creator"
        assert dep.head_of_department.start_date == date(2024,10,2)
        assert dep.head_of_department.salary == 30000
        assert dep.head_of_department.address == "123 Lane, Town, County"
    def test_department_id_created(self):
        with patch("employee_tracker.domain.department.new_id", return_value="dep") as mock_new_id:
            dep = Department(**valid_department_kwargs())

            mock_new_id.assert_called_once_with("dep")
            assert dep.id.startswith("dep")    

class TestDepartmentTypeValidations:
    @pytest.mark.parametrize(
        "field,value,error",
        [
            ("name", 123, "Name must be a string"),
            ("description", True, "Description must be a string"),
            ("head_of_department", "James", "Head of department must be a valid Employee object"),
        ],
    )
    def test_invalid_datatypes(self, field, value, error):
        kwargs = valid_department_kwargs()
        kwargs[field] = value

        with pytest.raises(TypeError, match=error):
            Department(**kwargs)

class TestDepartmentAddEmployee:
    def test_department_has_add_employee(self):
        assert hasattr(Department,"add_employee")