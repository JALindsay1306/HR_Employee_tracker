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

def make_row(**overrides):
    # A baseline "row" like you'd get from df.to_dict(orient="records")
        base = {
            "name": "per_1",
            "active": True,
        }
        base.update(overrides)
        return base


class TestPermissionCreation:
    def test_permission_can_be_created(self):
        per = Permission(**valid_permission_kwargs())
        assert hasattr(per,"name")
        assert hasattr(per,"active")

class TestPermissionTypeValidation:
     @pytest.mark.parametrize(
        "field,value,error",
        [
            ("name", 123, "Name must be a string"),
            ("active", 3.45, "active must be a boolean value"),
        ],
     )
     def test_invalid_datatypes(self, field, value, error):
        kwargs = valid_permission_kwargs()
        kwargs[field] = value

        with pytest.raises(TypeError, match=error):
            Permission(**kwargs)

class TestChangeName:
    def test_change_name_changes_name(self):
        per1 = Permission(**valid_permission_kwargs())
        per1.name = "New name"
        assert per1.name == "New name"
    def test_change_name_validates_string(self):
        per1 = Permission(**valid_permission_kwargs())
        with pytest.raises(TypeError,match="name must be a string"):
            per1.name = False
    def test_will_not_accept_same_name(self):
        per1 = Permission(**valid_permission_kwargs())
        per1.name = "New name"
        with pytest.raises(ValueError,match = "name is already New name"):
            per1.name = "New name"

class TestSetActive:
    def test_can_change_active_state(self):
        per1 = Permission(**valid_permission_kwargs())
        per1.active = True
        assert per1.active == True
        per1.active = False
        assert per1.active == False
    def test_rejects_invalid_input(self):
        per1 = Permission(**valid_permission_kwargs())
        with pytest.raises(TypeError,match="active must be a boolean value"):
             per1.active = 1234

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
        "active"
        }

        assert expected_keys.issubset(per1_row.keys())
    def test_values_are_correct(self):
        per1 = Permission(**valid_permission_kwargs())

        per1_row = per1.to_row()

        expected = {
            "name": "per_1",
            "active": False
        }
        assert per1_row == expected

class TestReturnFromStorage:
    def test_permission_has_from_row_method(self):
        assert hasattr(Permission,"from_row")
    def test_from_row_preserves_name(self):
        row = make_row(name="everything")
        perm = Permission.from_row(row)
        assert perm.name == "everything"
    def test_from_row_missing_active_defaults_to_None(self):
        row = make_row()
        row.pop("active")
        perm = Permission.from_row(row)
        assert perm.active == False
