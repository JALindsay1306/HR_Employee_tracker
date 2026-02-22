import pytest
from unittest.mock import patch
from datetime import date
import pandas as pd

from employee_tracker.domain.employee import Employee
from employee_tracker.utils.value_checkers import check_new_value
from employee_tracker.domain.permission import Permission
from employee_tracker.utils.ids import check_id


def valid_employee_kwargs():
    return dict(
        name="James",
        role="Creator",
        start_date=date(2024, 10, 2),
        salary=30000,
        address="123 Lane, Town, County",
        password_hash="zXl7n7B2cF9ZzC6bX5mJ8sQ2k1pLr4vTtYw9aBcDeFgHiJkLmNoPqRsTuVwXyZ12"
    )
def make_row(**overrides):
    # A baseline "row" like you'd get from df.to_dict(orient="records")
        base = {
            "id": "emp_1234abcd",
            "name": "James",
            "role": "Creator",
            "start_date": pd.Timestamp("2024-10-02"),
            "salary": 30000,
            "address": "123 Lane, Town, County",
            "permissions": "READ WRITE",
            "password_hash": "zXl7n7B2cF9ZzC6bX5mJ8sQ2k1pLr4vTtYw9aBcDeFgHiJkLmNoPqRsTuVwXyZ12"            
        }
        base.update(overrides)
        return base

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
    def test_new_employee_permissions_is_empty(self):
        emp = Employee(**valid_employee_kwargs())
        assert emp.permissions == []
    def test_employee_accepts_existing_id(self):
        emp = Employee(
            name="James",
            role="Me",
            start_date=date(2023,12,12),
            salary=12345,
            address="An Address",
            id= "emp_12345678",
            password="password"
        )
        assert emp.id == "emp_12345678"

class TestEmployeeTypeValidation:
    @pytest.mark.parametrize(
        "field,value,error",
        [
            ("name", 123, "Name must be a string"),
            ("role", True, "Role must be a string"),
            ("salary", "money", "Salary must be an integer"),
            ("address", None, "Address must be a string"),#
            ("id","emp_KKAS","Invalid ID")
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

class TestChangeName:
    def test_change_name_changes_name(self):
        emp = Employee(**valid_employee_kwargs())
        emp.name = "New Name"
        assert emp.name == "New Name"
    @patch("employee_tracker.domain.employee.check_new_value")
    def test_check_new_value_called(self,mock_check_value):
        emp = Employee(**valid_employee_kwargs())
        emp.name = "New Name"
        mock_check_value.assert_called_once_with(
            "New Name",
            "name",
            str,
            "James"
        )

class TestChangeRole:
    def test_change_role_changes_role(self):
        emp = Employee(**valid_employee_kwargs())
        emp.role = "New Role"
        assert emp.role == "New Role"
    @patch("employee_tracker.domain.employee.check_new_value")
    def test_check_new_value_called(self,mock_check_value):
        emp = Employee(**valid_employee_kwargs())
        emp.role = "New Role"
        mock_check_value.assert_called_once_with(
            "New Role",
            "role",
            str,
            "Creator"
        )

class TestChangeSalary:
    def test_change_salary_changes_salary(self):
        emp = Employee(**valid_employee_kwargs())
        emp.salary = 100000
        assert emp.salary == 100000
    @patch("employee_tracker.domain.employee.check_new_value")
    def test_check_new_value_called(self,mock_check_value):
        emp = Employee(**valid_employee_kwargs())
        emp.salary = 100000
        mock_check_value.assert_called_once_with(
            100000,
            "salary",
            int,
            30000
        )

class TestChangeAddress:
    def test_change_address_changes_address(self):
        emp = Employee(**valid_employee_kwargs())
        emp.address = "123 New Lane"
        assert emp.address == "123 New Lane"
    @patch("employee_tracker.domain.employee.check_new_value")
    def test_check_new_value_called(self,mock_check_value):
        emp = Employee(**valid_employee_kwargs())
        emp.address = "123 New Lane"
        mock_check_value.assert_called_once_with(
            "123 New Lane",
            "address",
            str,
            "123 Lane, Town, County"
        )

class TestAddPermission:
    def test_employee_has_add_permission(self):
        assert hasattr(Employee,"add_permission")
    def test_add_permission_adds_permission(self):
        emp = Employee(**valid_employee_kwargs())
        per = Permission("per_1")
        emp.add_permission(per)
        assert emp.permissions[0] == "per_1"
        per2 = Permission("per_2")
        emp.add_permission(per2)
        assert emp.permissions[1] == "per_2"
    def test_duplicate_permission_raises_error(self):
        emp = Employee(**valid_employee_kwargs())
        per = Permission("per_1")
        emp.add_permission(per)
        per2 = Permission("per_1")
        with pytest.raises(ValueError, match = "James already has the permission per_1, cannot add again"):
            emp.add_permission(per2)
    @patch("employee_tracker.domain.employee.check_new_value")
    def test_check_new_value_called(self,mock_check_value):
        emp = Employee(**valid_employee_kwargs())
        per = Permission("per_1")
        emp.add_permission(per)
        mock_check_value.assert_called_once_with(
            "per_1",
            "permission",
            str,
        )
    def test_non_permission_not_accepted(self):
        emp = Employee(**valid_employee_kwargs())
        emp2 = Employee(**valid_employee_kwargs())
        with pytest.raises(TypeError, match = "This value is not a permission, please check and try again"):
            emp.add_permission(emp2)

class TestRemovePermission:
    def test_employee_has_remove_permission_method(self):
        assert hasattr(Employee,"remove_permission")
    def test_remove_permission_removes_permissions(self):
        emp = Employee(**valid_employee_kwargs())
        per = Permission("per_1")
        per2 = Permission("per_2")
        emp.add_permission(per)
        emp.add_permission(per2)
        emp.remove_permission(per)
        assert len(emp.permissions) == 1
        assert "per_1" not in emp.permissions
    def test_cannot_remove_permission_not_in_list(self):
        emp = Employee(**valid_employee_kwargs())
        per = Permission("per_1")
        per2 = Permission("per_2")
        emp.add_permission(per)
        with pytest.raises(ValueError, match = "James does not have the permission per_2 to remove"):
           emp.remove_permission(per2)
    def test_invalid_input_rejected(self):
        emp = Employee(**valid_employee_kwargs())
        emp2 = Employee(**valid_employee_kwargs())
        per = Permission("per_1")
        emp.add_permission(per)
        with pytest.raises(TypeError, match = "This value is not a permission, please check and try again"):
            emp.remove_permission(emp2)

class TestWipePermissions:
    def test_employee_has_wipe_permissions_method(self):
        assert hasattr(Employee,"wipe_permissions")
    def test_removes_all_permissions(self):
        emp = Employee(**valid_employee_kwargs())
        per = Permission("per_1")
        per2 = Permission("per_2")
        per3 = Permission("per_3")
        emp.add_permission(per)
        emp.add_permission(per2)
        emp.add_permission(per3)
        emp.wipe_permissions()
        assert len(emp.permissions) == 0
    def test_raises_error_if_no_permissions_present(self):
        emp = Employee(**valid_employee_kwargs())
        with pytest.raises(ValueError, match = "no permissions to wipe"):
            emp.wipe_permissions()

class TestStoragePreparation:
    def test_employee_has_to_row_method(self):
        assert hasattr(Employee,"to_row")
    def test_to_row_method_returns_dict(self):
        emp1 = Employee(**valid_employee_kwargs())
        assert isinstance(emp1.to_row(),dict)
    def test_to_row_method_has_all_attrs(self):
        emp1 = Employee(**valid_employee_kwargs())
        emp1_row = emp1.to_row()
        expected_keys = {
        "id", 
        "name", 
        "role", 
        "start_date",
        "salary", 
        "address", 
        "password_hash",
        "permissions"
        }

        assert expected_keys.issubset(emp1_row.keys())
    def test_values_are_correct(self):
        emp1 = Employee(**valid_employee_kwargs())

        emp1_row = emp1.to_row()
        assert check_id(emp1_row.pop("id"), "emp")

        expected = {
            "name": "James",
            "role": "Creator",
            "start_date": date(2024, 10, 2),
            "salary": 30000,
            "address": "123 Lane, Town, County",
            "password_hash": "zXl7n7B2cF9ZzC6bX5mJ8sQ2k1pLr4vTtYw9aBcDeFgHiJkLmNoPqRsTuVwXyZ12",
            "permissions": " ".join(emp1.permissions),
        }
        assert emp1_row == expected
    def test_permissions_are_space_separated(self):
        emp1 = Employee(**valid_employee_kwargs())
        per1 = Permission("per_1")
        per2 = Permission("per_2")
        per3 = Permission("per_3")
        emp1.add_permission(per1)
        emp1.add_permission(per2)
        emp1.add_permission(per3)
        emp1_row = emp1.to_row()
        assert emp1_row["permissions"] == f"{per1.name} {per2.name} {per3.name}"
        permissions = emp1_row["permissions"].split(" ")
        assert permissions == [per1.name,per2.name,per3.name]

class TestReturnFromStorage:
    def test_employee_has_from_row_method(self):
        assert hasattr(Employee,"from_row")
    def test_from_row_preserves_id(self):
        row = make_row(id="emp_deadbeef")
        emp = Employee.from_row(row)
        assert emp.id == "emp_deadbeef"
    def test_from_row_accepts_date(self):
        row = make_row(start_date=date(2024, 10, 2))
        emp = Employee.from_row(row)
        assert emp.start_date == date(2024, 10, 2)
    def test_from_row_parses_permissions_string_to_list(self):
        row = make_row(permissions="READ WRITE ADMIN")
        emp = Employee.from_row(row)
        assert emp.permissions == ["READ", "WRITE", "ADMIN"]
    def test_from_row_empty_permissions_becomes_empty_list(self):
        row = make_row(permissions="")
        emp = Employee.from_row(row)
        assert emp.permissions == []
    def test_from_row_missing_permissions_defaults_to_empty_list(self):
        row = make_row()
        row.pop("permissions")
        emp = Employee.from_row(row)
        assert emp.permissions == []
    def test_from_row_salary_string_is_cast_to_int(self):
        row = make_row(salary="30000")
        emp = Employee.from_row(row)
        assert emp.salary == 30000
        assert isinstance(emp.salary, int)

