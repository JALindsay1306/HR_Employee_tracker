import pytest
from datetime import date
from unittest.mock import patch

from employee_tracker.domain.tracker import Tracker
from employee_tracker.domain.employee import Employee
from employee_tracker.domain.department import Department
from employee_tracker.domain.permission import Permission

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

example_dep = Department("test","testDes",Employee(**valid_employee_kwargs()).id)

employee_to_use = Employee(**valid_employee_kwargs())

def valid_department_kwargs():
    return dict(
        name="Finance",
        description = "It's where the money is",
        head_of_department = employee_to_use.id,
        parent_department = example_dep.id
    )

class TestTrackerCreation:
    def test_tracker_created_successfully(self):
        trk = Tracker()
        assert hasattr(trk,"employees")
        assert hasattr(trk,"departments")
        assert hasattr(trk,"permissions")



class TestCreateEmployee:
    def test_tracker_has_create_employee_method(self):
        assert hasattr(Tracker,"create_employee")
    @patch("employee_tracker.domain.tracker.Employee")
    def test_create_employee_calls_employee_constructor(self,mock_employee):
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
    def test_create_employee_adds_to_employees(self):
        trk = Tracker()
        emp = trk.create_employee("John","Boss",date(2024, 10, 2),50000,"My Address")
        assert len(trk.employees) == 1
        assert trk.employees[emp.id].name == "John"
    def test_created_employee_is_employee_class(self):
        trk = Tracker()
        emp = trk.create_employee("John","Boss",date(2024, 10, 2),50000,"My Address")
        assert isinstance(trk.employees[emp.id],Employee)

class TestCreateEmployeeTypeValidation:
    @pytest.mark.parametrize(
        "field,value,error",
        [
            ("name", 123, "Name must be a string"),
            ("role", 3.45, "Role must be a string"),
            ("start_date","today","start_date must be a date"),
            ("salary","a lot","Salary must be an integer"),
            ("address",43212,"Address must be a string"),
            ("permissions", "All","permissions must be a list of permission ids"),
            ("permissions", ["33"],"permissions in list must be valid permission ids")

        ],
     )

    def test_invalid_datatypes(self, field, value, error):
        trk = Tracker()
        kwargs = valid_employee_kwargs()
        kwargs[field] = value

        with pytest.raises(TypeError, match=error):
            trk.create_employee(**kwargs)
    
    
class TestCreateDepartment:
    def test_tracker_has_create_department_method(self):
        assert hasattr(Tracker,"create_department")
    @patch("employee_tracker.domain.tracker.Department")
    def test_create_department_calls_department_constructor(self,mock_department):
        trk = Tracker()
        emp = trk.create_employee("John","Boss",date(2024, 10, 2),50000,"My Address")
        dep = trk.create_department("Finance","Where the money is",emp.id)
        mock_department.assert_called_once_with(
            "Finance",
            "Where the money is",
            emp.id,
            None,
            None
        )
    def test_create_department_adds_to_departments(self):
        trk = Tracker()
        emp = trk.create_employee("John","Boss",date(2024, 10, 2),50000,"My Address")
        dep = trk.create_department("Finance","Where the money is",emp.id)
        assert len(trk.departments) == 1
        assert trk.departments[dep.id].name == "Finance"
    def test_created_department_is_department_class(self):
        trk = Tracker()
        emp = trk.create_employee("John","Boss",date(2024, 10, 2),50000,"My Address")
        dep = trk.create_department("Finance","Where the money is",emp.id)
        assert isinstance(trk.departments[dep.id],Department)

class TestCreateDepartmentTypeValidation:
    @pytest.mark.parametrize(
        "field,value,error",
        [
            ("name", 123, "Name must be a string"),
            ("description", 3.45, "Description must be a string"),
            ("head_of_department","today","head_of_department must be a valid employee id"),
            ("parent_department","today","parent_department must be a valid department id"),
            ("members", "All","members must be a list of employee ids"),
            ("members", ["33","445"],"members in list must be valid employee ids")

        ],
     )

    def test_invalid_datatypes(self, field, value, error):
        trk = Tracker()

        kwargs = valid_department_kwargs()
        kwargs[field] = value

        with pytest.raises(TypeError, match=error):
            trk.create_department(**kwargs)

class TestCreatePermission:
    def test_tracker_has_create_permission_method(self):
        assert hasattr(Tracker,"create_permission")
    @patch("employee_tracker.domain.tracker.Permission")
    def test_create_permission_calls_permission_constructor(self,mock_permission):
        trk = Tracker()
        emp = trk.create_employee("John","Boss",date(2024, 10, 2),50000,"My Address")
        dep = trk.create_department("Finance","Where the money is",emp.id)
        per = trk.create_permission("admin",dep.id)
        mock_permission.assert_called_once_with(
            "admin",
            dep.id,
        )
    def test_create_permission_adds_to_permissions(self):
        trk = Tracker()
        emp = trk.create_employee("John","Boss",date(2024, 10, 2),50000,"My Address")
        dep = trk.create_department("Finance","Where the money is",emp.id)
        per = trk.create_permission("admin",dep.id)
        assert len(trk.permissions) == 1
        assert trk.permissions[per.name].name == "admin"
    def test_created_permission_is_permission_class(self):
        trk = Tracker()
        emp = trk.create_employee("John","Boss",date(2024, 10, 2),50000,"My Address")
        dep = trk.create_department("Finance","Where the money is",emp.id)
        per = trk.create_permission("admin",dep.id)
        assert isinstance(trk.permissions[per.name],Permission)

class TestCreatePermissionTypeValidation:
    @pytest.mark.parametrize(
        "field,value,error",
        [
            ("name", 123, "Name must be a string"),
            ("department","today","department must be a valid department id"),
        ],
     )

    def test_invalid_datatypes(self, field, value, error):
        trk = Tracker()
        emp = trk.create_employee("John","Boss",date(2024, 10, 2),50000,"My Address")
        dep = trk.create_department("Finance","Where the money is",emp.id)
        kwargs = valid_permission_kwargs()
        kwargs[field] = value

        with pytest.raises(TypeError, match=error):
            trk.create_permission(**kwargs)
    
