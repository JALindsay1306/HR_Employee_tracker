import pytest
from datetime import date
from unittest.mock import patch, MagicMock
import pandas as pd

from employee_tracker.domain.tracker import Tracker
from employee_tracker.domain.employee import Employee
from employee_tracker.domain.department import Department
from employee_tracker.domain.permission import Permission
from employee_tracker.storage.storage import create_dataframe, write_csv, read_csv
import employee_tracker.domain.tracker as tracker_module


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
            ("permissions", "All","permissions must be a list of permission names"),
            ("permissions", ["33"],"permissions in list must be valid permission names")

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

class TestListDepartments:
    def test_tracker_has_list_departments_method(self):
        assert hasattr(Tracker,"list_departments")
    def test_list_departments_returns_list(self):
        trk = Tracker()
        kwargs = valid_department_kwargs()
        trk.create_department(**kwargs)
        trk.create_department(**kwargs)
        trk.create_department(**kwargs)
        trk.create_department(**kwargs)
        department_list = trk.list_departments()
        assert isinstance(department_list,list)
    def test_list_departments_returns_all_departments_when_called_with_no_arguments(self):
        trk = Tracker()
        kwargs = valid_department_kwargs()
        trk.create_department(**kwargs)
        trk.create_department(**kwargs)
        trk.create_department(**kwargs)
        trk.create_department(**kwargs)
        department_list = trk.list_departments()
        assert len(department_list) == 4
        for department in department_list:
            assert isinstance(department,Department)
    def test_returned_departments_are_correct(self):
        trk = Tracker()
        kwargs = valid_department_kwargs()
        dep_1 = trk.create_department(**kwargs)
        dep_2 = trk.create_department(**kwargs)
        dep_3 = trk.create_department(**kwargs)
        dep_4 = trk.create_department(**kwargs)
        department_list = trk.list_departments()
        assert dep_1.id == department_list[0].id
        assert dep_2.name == department_list[0].name
        assert dep_3.description == department_list[0].description
        assert dep_4.head_of_department == department_list[0].head_of_department
    def test_can_search_by_name(self):
        trk = Tracker()
        kwargs = valid_department_kwargs()
        dep_1 = trk.create_department(**kwargs)
        trk.departments[dep_1.id].name = "IT"
        dep_2 = trk.create_department(**kwargs)
        trk.departments[dep_2.id].name = "New IT"
        dep_3 = trk.create_department(**kwargs)
        trk.departments[dep_3.id].name = "Shipping"
        dep_4 = trk.create_department(**kwargs)
        trk.departments[dep_4.id].name = "Board"
        department_list = trk.list_departments(name_search="IT")
        assert len(department_list) == 2
        assert department_list[0].name == "IT" and department_list[1].name == "New IT"
    def test_can_search_by_description(self):
        trk = Tracker()
        kwargs = valid_department_kwargs()
        dep_1 = trk.create_department(**kwargs)
        trk.departments[dep_1.id].description = "Make computers work"
        dep_2 = trk.create_department(**kwargs)
        trk.departments[dep_2.id].descripton = "More complex"
        dep_3 = trk.create_department(**kwargs)
        trk.departments[dep_3.id].description = "Move stuff"
        dep_4 = trk.create_department(**kwargs)
        trk.departments[dep_4.id].description = "Don't really work"
        department_list = trk.list_departments(description_search="work")
        assert len(department_list) == 2
        assert department_list[0].description == "Make computers work" and department_list[1].description == "Don't really work"
    def test_can_search_by_head_of_department(self):
        trk = Tracker()
        ekwargs = valid_employee_kwargs()
        dkwargs = valid_department_kwargs()
        emp_1 = trk.create_employee(**ekwargs)
        emp_2 = trk.create_employee(**ekwargs)
        emp_3 = trk.create_employee(**ekwargs)
        emp_4 = trk.create_employee(**ekwargs)

        dep_1 = trk.create_department(**dkwargs)
        trk.departments[dep_1.id].change_head_of_department(emp_1)
        dep_2 = trk.create_department(**dkwargs)
        trk.departments[dep_2.id].change_head_of_department(emp_2)
        dep_3 = trk.create_department(**dkwargs)
        trk.departments[dep_3.id].change_head_of_department(emp_3)
        dep_4 = trk.create_department(**dkwargs)
        trk.departments[dep_4.id].change_head_of_department(emp_4)
        department_list = trk.list_departments(head_of_department_search=emp_2.id)
        assert len(department_list) == 1
        assert department_list[0].head_of_department == emp_2.id
    def test_can_search_by_parent_department(self):
        trk = Tracker()
        kwargs = valid_department_kwargs()
        dep_1 = trk.create_department(**kwargs)
        dep_2 = trk.create_department(**kwargs)
        dep_3 = trk.create_department(**kwargs)
        dep_4 = trk.create_department(**kwargs)
        
        trk.departments[dep_1.id].set_parent_department(dep_2)
        trk.departments[dep_2.id].set_parent_department(dep_3)
        trk.departments[dep_3.id].set_parent_department(dep_4)
        trk.departments[dep_4.id].set_parent_department(dep_2)
        department_list = trk.list_departments(parent_department_search=dep_2.id)
        assert len(department_list) == 2
        assert department_list[0].parent_department == dep_2.id and department_list[1].parent_department == dep_2.id
        
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

class TestStorageManagement:
    def test_tracker_has_save_to_storage_method(self):
        assert hasattr(Tracker,"save_to_storage")
    def test_tracker_has_load_from_storage_method(self):
        assert hasattr(Tracker,"load_from_storage")
    def test_save_calls_write_csv(self,monkeypatch):
        tracker = Tracker()

        fake_emp = MagicMock()
        fake_emp.to_row.return_value = {"id": "emp_x"}

        tracker.employees["emp_x"] = fake_emp

        create_df_mock = MagicMock(return_value=pd.DataFrame([{"id": "emp_x"}]))
        write_mock = MagicMock()

        monkeypatch.setattr(tracker_module, "create_dataframe", create_df_mock)
        monkeypatch.setattr(tracker_module, "write_csv", write_mock)

        tracker.save_to_storage()

        create_df_mock.assert_called_once()
        write_mock.assert_called_once()
    
    def test_load_calls_from_row(self, monkeypatch):
        emp_df = pd.DataFrame([{
            "id": "emp_aaaa1111",
            "name": "James",
            "role": "Creator",
            "start_date": pd.Timestamp("2024-10-02"),
            "salary": 100,
            "address": "x",
            "permissions": "",
        }])

        def fake_read_csv(file_type: str):
            if file_type == "employees":
                return emp_df
            if file_type == "departments":
                return pd.DataFrame(columns=["id", "name", "description", "head_of_department", "parent_department", "members"])
            if file_type == "permissions":
                return pd.DataFrame(columns=["name", "department"])
            raise ValueError(file_type)

        monkeypatch.setattr(tracker_module, "read_csv", fake_read_csv)

        fake_emp = MagicMock()
        fake_emp.id = "emp_aaaa1111"

        emp_from_row = MagicMock(return_value=fake_emp)
        monkeypatch.setattr(tracker_module.Employee, "from_row", emp_from_row)
        
        monkeypatch.setattr(tracker_module.Department, "from_row", MagicMock())
        monkeypatch.setattr(tracker_module.Permission, "from_row", MagicMock())

        tracker = Tracker.load_from_storage()

        emp_from_row.assert_called_once_with(emp_df.to_dict(orient="records")[0])
        assert tracker.employees["emp_aaaa1111"] is fake_emp
