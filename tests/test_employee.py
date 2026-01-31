import pytest
from unittest.mock import patch

from employee_tracker.domain.employee import Employee
from datetime import date

def valid_employee_kwargs():
    return dict(
        name="James",
        role="Creator",
        start_date=date(2024, 10, 2),
        salary=30000,
        address="123 Lane, Town, County",
    )

class TestEmployeeCreation:
    def test_employee_can_be_created(self):
        emp = Employee(**valid_employee_kwargs())
        assert hasattr(emp,"id")
        assert emp.name == "James"
        assert emp.role == "Creator"
        assert emp.start_date == date(2024,10,2)
        assert emp.salary == 30000
        assert emp.address == "123 Lane, Town, County"
    def test_employee_id_created(self):
        with patch("employee_tracker.domain.employee.new_id", return_value="emp") as mock_new_id:
            emp = Employee(**valid_employee_kwargs())

            mock_new_id.assert_called_once_with("emp")
            assert emp.id.startswith("emp")
    def test_new_employee_is_enabled(self):
        emp = Employee(**valid_employee_kwargs())
        assert emp.enabled == True
    def test_new_employee_has_no_permissions(self):
        emp = Employee(**valid_employee_kwargs())
        assert emp.permissions == None

class TestEmployeeTypeValidation:
    @pytest.mark.parametrize(
        "field,value,error",
        [
            ("name", 123, "Name must be a string"),
            ("role", True, "Role must be a string"),
            ("salary", "money", "Salary must be an integer"),
            ("address", None, "Address must be a string"),
        ],
    )
    def test_invalid_datatypes(self, field, value, error):
        kwargs = valid_employee_kwargs()
        kwargs[field] = value

        with pytest.raises(TypeError, match=error):
            Employee(**kwargs)

class TestEmployeeSalaryBump:
    def test_employee_has_salary_bump(self):
        assert hasattr(Employee,"salary_bump")
    def test_salary_bump_works(self):
        emp = Employee(**valid_employee_kwargs())
        emp.salary_bump(10)
        assert emp.salary == 33000

    def test_salary_bump_rounds(self):
        emp = Employee(**valid_employee_kwargs())
        emp.salary_bump(11.555)
        #Python uses bankers rounding (to nearest even no.)
        assert emp.salary == 33466
        assert isinstance(emp.salary, int)

class TestEmployeeEnableToggle:
    def test_employee_has_enable_toggle(self):
        assert hasattr(Employee,"enable_disable")
    def test_employee_enable_toggle(self):
        emp = Employee(**valid_employee_kwargs())
        emp.enable_disable()
        assert emp.enabled == False
        emp.enable_disable()
        assert emp.enabled == True
    