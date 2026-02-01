import pytest
from unittest.mock import patch
from datetime import date

from employee_tracker.domain.employee import Employee
from employee_tracker.utils.value_checkers import check_new_value
from employee_tracker.domain.permission import Permission


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

class TestChangeName:
    def test_employee_has_name_change_method(self):
        assert hasattr(Employee,"change_name")
    def test_change_name_changes_name(self):
        emp = Employee(**valid_employee_kwargs())
        emp.change_name("New Name")
        assert emp.name == "New Name"
    @patch("employee_tracker.domain.employee.check_new_value")
    def test_check_new_value_called(self,mock_check_value):
        emp = Employee(**valid_employee_kwargs())
        emp.change_name("New Name")
        mock_check_value.assert_called_once_with(
            "New Name",
            "name",
            str,
            "James"
        )

class TestChangeRole:
    def test_employee_has_role_change_method(self):
        assert hasattr(Employee,"change_role")
    def test_change_name_changes_name(self):
        emp = Employee(**valid_employee_kwargs())
        emp.change_role("New Role")
        assert emp.role == "New Role"
    @patch("employee_tracker.domain.employee.check_new_value")
    def test_check_new_value_called(self,mock_check_value):
        emp = Employee(**valid_employee_kwargs())
        emp.change_role("New Role")
        mock_check_value.assert_called_once_with(
            "New Role",
            "role",
            str,
            "Creator"
        )

class TestChangeSalary:
    def test_employee_has_salary_change_method(self):
        assert hasattr(Employee,"change_salary")
    def test_change_salary_changes_salary(self):
        emp = Employee(**valid_employee_kwargs())
        emp.change_salary(100000)
        assert emp.salary == 100000
    @patch("employee_tracker.domain.employee.check_new_value")
    def test_check_new_value_called(self,mock_check_value):
        emp = Employee(**valid_employee_kwargs())
        emp.change_salary(100000)
        mock_check_value.assert_called_once_with(
            100000,
            "salary",
            int,
            30000
        )

class TestChangeAddress:
    def test_employee_has_address_change_method(self):
        assert hasattr(Employee,"change_address")
    def test_change_address_changes_address(self):
        emp = Employee(**valid_employee_kwargs())
        emp.change_address("123 New Lane")
        assert emp.address == "123 New Lane"
    @patch("employee_tracker.domain.employee.check_new_value")
    def test_check_new_value_called(self,mock_check_value):
        emp = Employee(**valid_employee_kwargs())
        emp.change_address("123 New Lane")
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