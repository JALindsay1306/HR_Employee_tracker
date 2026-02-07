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
    
class TestListEmployees:
    def test_tracker_has_list_employees_method(self):
        assert hasattr(Tracker,"list_employees")
    def test_list_employees_returns_list(self):
        trk = Tracker()
        kwargs = valid_employee_kwargs()
        trk.create_employee(**kwargs)
        trk.create_employee(**kwargs)
        trk.create_employee(**kwargs)
        trk.create_employee(**kwargs)
        employee_list = trk.list_employees()
        assert isinstance(employee_list,list)
    def test_list_employees_returns_all_employees_when_called_with_no_arguments(self):
        trk = Tracker()
        kwargs = valid_employee_kwargs()
        trk.create_employee(**kwargs)
        trk.create_employee(**kwargs)
        trk.create_employee(**kwargs)
        trk.create_employee(**kwargs)
        employee_list = trk.list_employees()
        assert len(employee_list) == 4
        for employee in employee_list:
            assert isinstance(employee,Employee)
    def test_returned_employees_are_correct(self):
        trk = Tracker()
        kwargs = valid_employee_kwargs()
        emp_1 = trk.create_employee(**kwargs)
        emp_2 = trk.create_employee(**kwargs)
        emp_3 = trk.create_employee(**kwargs)
        emp_4 = trk.create_employee(**kwargs)
        employee_list = trk.list_employees()
        assert emp_1.id == employee_list[0].id
        assert emp_2.name == employee_list[0].name
        assert emp_3.role == employee_list[0].role
        assert emp_4.salary == employee_list[0].salary
    def test_can_search_by_name(self):
        trk = Tracker()
        kwargs = valid_employee_kwargs()
        emp_1 = trk.create_employee(**kwargs)
        trk.employees[emp_1.id].name = "Steve"
        emp_2 = trk.create_employee(**kwargs)
        trk.employees[emp_2.id].name = "Steph"
        emp_3 = trk.create_employee(**kwargs)
        trk.employees[emp_3.id].name = "Charlotte"
        emp_4 = trk.create_employee(**kwargs)
        trk.employees[emp_4.id].name = "John"
        employee_list = trk.list_employees(name_search="Ste")
        assert len(employee_list) == 2
        assert employee_list[0].name == "Steve" and employee_list[1].name == "Steph"
    def test_can_search_by_role(self):
        trk = Tracker()
        kwargs = valid_employee_kwargs()
        emp_1 = trk.create_employee(**kwargs)
        trk.employees[emp_1.id].role = "Boss"
        emp_2 = trk.create_employee(**kwargs)
        trk.employees[emp_2.id].role = "Cleaner"
        emp_3 = trk.create_employee(**kwargs)
        trk.employees[emp_3.id].role = "Dogsbody"
        emp_4 = trk.create_employee(**kwargs)
        trk.employees[emp_4.id].role = "Big Boss"
        employee_list = trk.list_employees(role_search="Boss")
        assert len(employee_list) == 2
        assert employee_list[0].role == "Boss" and employee_list[1].role == "Big Boss"
    def test_can_search_by_min_start_date(self):
        trk = Tracker()
        kwargs = valid_employee_kwargs()
        emp_1 = trk.create_employee(**kwargs)
        trk.employees[emp_1.id].start_date = date(2024, 10, 2)
        emp_2 = trk.create_employee(**kwargs)
        trk.employees[emp_2.id].start_date = date(2025, 1, 2)
        emp_3 = trk.create_employee(**kwargs)
        trk.employees[emp_3.id].start_date = date(2023, 10, 4)
        emp_4 = trk.create_employee(**kwargs)
        trk.employees[emp_4.id].start_date = date(2022, 12, 15)
        employee_list = trk.list_employees(min_date=date(2024,1,1))
        assert len(employee_list) == 2
        assert employee_list[0].start_date == date(2024, 10, 2) and employee_list[1].start_date == date(2025, 1, 2)
    def test_can_search_by_max_start_date(self):
        trk = Tracker()
        kwargs = valid_employee_kwargs()
        emp_1 = trk.create_employee(**kwargs)
        trk.employees[emp_1.id].start_date = date(2024, 10, 2)
        emp_2 = trk.create_employee(**kwargs)
        trk.employees[emp_2.id].start_date = date(2025, 1, 2)
        emp_3 = trk.create_employee(**kwargs)
        trk.employees[emp_3.id].start_date = date(2023, 10, 4)
        emp_4 = trk.create_employee(**kwargs)
        trk.employees[emp_4.id].start_date = date(2022, 12, 15)
        employee_list = trk.list_employees(max_date=date(2024,1,1))
        assert len(employee_list) == 2
        assert employee_list[0].start_date == date(2023, 10, 4) and employee_list[1].start_date == date(2022, 12, 15)
    def test_can_search_by_min_salary(self):
        trk = Tracker()
        kwargs = valid_employee_kwargs()
        emp_1 = trk.create_employee(**kwargs)
        trk.employees[emp_1.id].salary = 40000
        emp_2 = trk.create_employee(**kwargs)
        trk.employees[emp_2.id].salary = 60000
        emp_3 = trk.create_employee(**kwargs)
        trk.employees[emp_3.id].salary = 80000
        emp_4 = trk.create_employee(**kwargs)
        trk.employees[emp_4.id].salary = 150000
        employee_list = trk.list_employees(min_salary=100000)
        assert len(employee_list) == 1
        assert employee_list[0].salary == 150000
    def test_can_search_by_max_salary(self):
        trk = Tracker()
        kwargs = valid_employee_kwargs()
        emp_1 = trk.create_employee(**kwargs)
        trk.employees[emp_1.id].salary = 40000
        emp_2 = trk.create_employee(**kwargs)
        trk.employees[emp_2.id].salary = 60000
        emp_3 = trk.create_employee(**kwargs)
        trk.employees[emp_3.id].salary = 80000
        emp_4 = trk.create_employee(**kwargs)
        trk.employees[emp_4.id].salary = 150000
        employee_list = trk.list_employees(max_salary=50000)
        assert len(employee_list) == 1
        assert employee_list[0].salary == 40000
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
    
