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
     )
def valid_department_kwargs():
    return dict(
        name="Finance",
        description = "It's where the money is",
        head_of_department = Employee(**valid_employee_kwargs()).id
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

class TestChangeName:
    def test_permission_has_change_name_method(self):
        assert hasattr(Permission,"change_name")
    def test_change_name_changes_name(self):
        per1 = Permission(**valid_permission_kwargs())
        per1.change_name("New name")
        assert per1.name == "New name"
    def test_change_name_validates_string(self):
        per1 = Permission(**valid_permission_kwargs())
        with pytest.raises(TypeError,match="name must be a string"):
            per1.change_name(1234)
    def test_will_not_accept_same_name(self):
        per1 = Permission(**valid_permission_kwargs())
        per1.change_name("New name")
        with pytest.raises(ValueError,match = "name is already New name"):
            per1.change_name("New name")

class TestAddDepartment:
    def test_permission_has_add_department_method(self):
        assert hasattr(Permission,"add_department")
    def test_add_department_adds_department_id(self):
        per1 = Permission(**valid_permission_kwargs())
        dep1 = Department(**valid_department_kwargs())
        per1.add_department(dep1)
        assert per1.department == dep1.id
    def test_will_not_accept_non_department(self):
        per1 = Permission(**valid_permission_kwargs())
        per2 = Permission(**valid_permission_kwargs())
        with pytest.raises(TypeError,match = "department must be a Department"):
            per1.add_department(per2)
    def test_id_checked_for_validity(self):
        with patch("employee_tracker.domain.permission.check_id", return_value="per") as mock_check_id:
            dep1 = Department(**valid_department_kwargs())
            per1 = Permission(**valid_permission_kwargs())
            per1.add_department(dep1)
            mock_check_id.assert_called_once_with(dep1.id,"dep")
    def test_rejects_invalid_id(self):
        dep1 = Department(**valid_department_kwargs())
        per1 = Permission(**valid_permission_kwargs())
        dep1.id = "BadID"
        with pytest.raises(ValueError,match="invalid ID"):
             per1.add_department(dep1)
    def test_replaces_old_department_with_new(self):
        per1 = Permission(**valid_permission_kwargs())
        dep1 = Department(**valid_department_kwargs())
        dep2 = Department(**valid_department_kwargs())
        per1.add_department(dep1)
        per1.add_department(dep2)
        assert per1.department == dep2.id
    def test_does_not_replace_with_same_department(self):
        per1 = Permission(**valid_permission_kwargs())
        dep1 = Department(**valid_department_kwargs())
        per1.add_department(dep1)
        with pytest.raises(ValueError,match = f"{dep1.name} is already the department, cannot replace with itself"):
            per1.add_department(dep1)

class TestRemoveDepartment:
    def test_permission_has_remove_department_method(self):
        assert hasattr(Permission,"remove_department")
    def test_remove_department_removes_department(self):
        per1 = Permission(**valid_permission_kwargs())
        dep1 = Department(**valid_department_kwargs())
        per1.add_department(dep1)
        per1.remove_department()
        assert per1.department == None
    def test_raises_error_when_no_department_present(self):
        per1 = Permission(**valid_permission_kwargs())
        with pytest.raises(ValueError,match="no department to remove"):
            per1.remove_department()

class TestStoragePreparation:
    def test_permission_has_to_row_method(self):
        assert hasattr(Permission,"to_row")
    def test_to_row_method_returns_dict(self):
        per1 = Permission(**valid_permission_kwargs())
        assert isinstance(per1.to_row(),dict)
    def test_to_row_method_has_all_attrs(self):
        per1 = Permission(**valid_permission_kwargs())
        per1_row = per1.to_row()
        expected_keys = { 
        "name", 
        "department"
        }

        assert expected_keys.issubset(per1_row.keys())
    def test_values_are_correct(self):
        per1 = Permission(**valid_permission_kwargs())
        dep1 = Department(**valid_department_kwargs())
        per1.add_department(dep1)

        per1_row = per1.to_row()

        expected = {
            "name": "per_1",
            "department": dep1.id
        }
        assert per1_row == expected