import pytest
from unittest.mock import patch

from datetime import date
from employee_tracker.domain.department import Department
from employee_tracker.domain.employee import Employee
from employee_tracker.utils.ids import check_id

def valid_employee_kwargs():
    return dict(
        name="James",
        role="Creator",
        start_date=date(2024, 10, 2),
        salary=30000,
        address="123 Lane, Town, County",
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


class TestDepartmentCreation:
    def test_department_can_be_created(self):
        dep = Department(**valid_department_kwargs())
        assert dep.name == "Finance"
        assert dep.description == "It's where the money is"
        assert dep.head_of_department == employee_to_use.id
        assert dep.parent_department == example_dep.id
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
            ("head_of_department", 123, "Head of department must be a string"),
            ("parent_department",False, "Parent Department must be a str or none")
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
    def test_add_employee_adds_employee_id(self):
        dep = Department(**valid_department_kwargs())
        emp1 = Employee(**valid_employee_kwargs())
        dep.add_employee(emp1)
        assert dep.members[0] == emp1.id
    def test_add_amployee_adds_multiple_employees(self):
        dep = Department(**valid_department_kwargs())
        emp1 = Employee(**valid_employee_kwargs())
        emp2 = Employee(**valid_employee_kwargs())
        emp3 = Employee(**valid_employee_kwargs())
        emp4 = Employee(**valid_employee_kwargs())
        emp5 = Employee(**valid_employee_kwargs())
        dep.add_employee(emp1)
        dep.add_employee(emp2)
        dep.add_employee(emp3)
        dep.add_employee(emp4)
        dep.add_employee(emp5)
        assert len(dep.members) == 5
    def test_does_not_accept_non_employees(self):
        dep1 = Department(**valid_department_kwargs())
        dep2 = Department(**valid_department_kwargs())
        with pytest.raises(TypeError,match = "Must be a valid Employee object"):
            dep1.add_employee(dep2)
    def test_does_not_accept_duplicates(self):
        dep = Department(**valid_department_kwargs())
        emp1 = Employee(**valid_employee_kwargs())
        dep.add_employee(emp1)
        with pytest.raises(ValueError,match=f"Employee ID {emp1.id} already in {dep.name}, cannot add again"):
            dep.add_employee(emp1)

class TestDepartmentListEmployees:
    def test_department_has_list_employees_method(self):
        assert hasattr(Department,"list_employees")
    def test_list_employees_returns_ids(self):
        dep = Department(**valid_department_kwargs())
        emp1 = Employee(**valid_employee_kwargs())
        emp2 = Employee(**valid_employee_kwargs())
        emp3 = Employee(**valid_employee_kwargs())
        dep.add_employee(emp1)
        dep.add_employee(emp2)
        dep.add_employee(emp3)
        emps = dep.list_employees()
        for emp in emps:
            assert check_id(emp,"emp")
    def test_list_employees_returns_all_employees(self):
        dep = Department(**valid_department_kwargs())
        emp1 = Employee(**valid_employee_kwargs())
        emp2 = Employee(**valid_employee_kwargs())
        emp3 = Employee(**valid_employee_kwargs())
        dep.add_employee(emp1)
        dep.add_employee(emp2)
        dep.add_employee(emp3)
        emps = dep.list_employees()
        assert emps == [emp1.id,emp2.id,emp3.id]
    def test_no_employees_raises_error(self):
        dep = Department(**valid_department_kwargs())
        with pytest.raises(ValueError,match="No employees in department"):
            dep.list_employees()
class TestRemoveEmployees:
    def test_department_has_remove_employee_method(self):
        assert hasattr(Department,"remove_employee")
    def test_remove_employee_removes_employee(self):
        dep = Department(**valid_department_kwargs())
        emp1 = Employee(**valid_employee_kwargs())
        emp2 = Employee(**valid_employee_kwargs())
        emp3 = Employee(**valid_employee_kwargs())
        dep.add_employee(emp1)
        dep.add_employee(emp2)
        dep.add_employee(emp3)
        dep.remove_employee(emp1.id)
        assert emp1.id not in dep.list_employees()
    def test_id_checked_for_validity(self):
        with patch("employee_tracker.domain.department.check_id", return_value="dep") as mock_check_id:
            dep = Department(**valid_department_kwargs())
            emp1 = Employee(**valid_employee_kwargs())
            emp2 = Employee(**valid_employee_kwargs())
            emp3 = Employee(**valid_employee_kwargs())
            dep.add_employee(emp1)
            dep.add_employee(emp2)
            dep.add_employee(emp3)
            dep.remove_employee(emp1.id)
            mock_check_id.assert_called_once_with(emp1.id,"emp")
    def test_rejects_invalid_id(self):
        dep = Department(**valid_department_kwargs())
        emp1 = Employee(**valid_employee_kwargs())
        emp2 = Employee(**valid_employee_kwargs())
        emp3 = Employee(**valid_employee_kwargs())
        dep.add_employee(emp1)
        dep.add_employee(emp2)
        dep.add_employee(emp3)
        with pytest.raises(ValueError,match="invalid ID"):
            dep.remove_employee("ID123")
    def test_raises_error_if_employee_not_present(self):
        dep = Department(**valid_department_kwargs())
        emp1 = Employee(**valid_employee_kwargs())
        emp2 = Employee(**valid_employee_kwargs())
        emp3 = Employee(**valid_employee_kwargs())
        dep.add_employee(emp1)
        dep.add_employee(emp2)
        with pytest.raises(ValueError,match=f"{emp3.id} not in department, cannot remove"):
            dep.remove_employee(emp3.id)
    def test_removing_last_employee_returns_message(self):
        dep = Department(**valid_department_kwargs())
        emp1 = Employee(**valid_employee_kwargs())
        dep.add_employee(emp1)
        assert dep.remove_employee(emp1.id) == "Last employee removed, department empty"

class TestUpdateName:
    def test_department_has_update_name(self):
        assert hasattr(Department,"update_name")
    def test_updates_name(self):
        dep = Department(**valid_department_kwargs())
        dep.update_name("New")
        assert dep.name == "New"
    def test_enforces_string_requirement(self):
        dep = Department(**valid_department_kwargs())
        with pytest.raises(TypeError,match="name must be a string"):
            dep.update_name(True)

class TestUpdateDescription:
    def test_department_has_update_description(self):
        assert hasattr(Department,"update_description")
    def test_updates_description(self):
        dep = Department(**valid_department_kwargs())
        dep.update_description("New")
        assert dep.description == "New"
    def test_enforces_string_requirement(self):
        dep = Department(**valid_department_kwargs())
        with pytest.raises(TypeError,match="description must be a string"):
            dep.update_description(True)
class TestChangeDepartmentHead:
    def test_department_has_change_department_head_method(self):
        assert hasattr(Department,"change_head_of_department")
    def test_change_department_head_updates_department_head(self):
        dep = Department(**valid_department_kwargs())
        emp1 = Employee(**valid_employee_kwargs())
        dep.change_head_of_department(emp1)
        assert dep.head_of_department == emp1.id
    def test_head_of_department_must_be_an_employee(self):
        dep1 = Department(**valid_department_kwargs())
        dep2 = Department(**valid_department_kwargs())
        with pytest.raises(TypeError,match="head of department must be an employee"):
            dep1.change_head_of_department(dep2)
    def test_id_checked_for_validity(self):
        with patch("employee_tracker.domain.department.check_id", return_value="dep") as mock_check_id:
            dep = Department(**valid_department_kwargs())
            emp1 = Employee(**valid_employee_kwargs())
            dep.change_head_of_department(emp1)
            mock_check_id.assert_called_once_with(emp1.id,"emp")
    def test_rejects_invalid_id(self):
        dep = Department(**valid_department_kwargs())
        emp1 = Employee(**valid_employee_kwargs())
        emp1.id = "BadID"
        with pytest.raises(ValueError,match="invalid ID"):
             dep.change_head_of_department(emp1)
    def test_does_not_replace_with_same_person(self):
        dep = Department(**valid_department_kwargs())
        emp1 = Employee(**valid_employee_kwargs())
        dep.change_head_of_department(emp1)
        with pytest.raises(ValueError,match=f"{emp1.name} \\({emp1.id}\\) is already head of department"):
            dep.change_head_of_department(emp1)
class TestSetParentDepartment:
    def test_department_has_set_parent_department_method(self):
        assert hasattr(Department,"set_parent_department")
    def test_set_parent_department_sets_parent_department(self):    
        dep1 = Department(**valid_department_kwargs())
        dep2 = Department(**valid_department_kwargs())
        dep1.set_parent_department(dep2)
        assert dep1.parent_department == dep2.id
    def test_does_not_accept_duplicate(self):
        dep1 = Department(**valid_department_kwargs())
        dep2 = Department(**valid_department_kwargs())
        dep1.set_parent_department(dep2)
        with pytest.raises(ValueError,match=f"{dep2.name} \\({dep2.id}\\) is already the parent department"):
            dep1.set_parent_department(dep2)
    def test_does_not_accept_non_departments(self):
        dep1 = Department(**valid_department_kwargs())
        emp1 = Employee(**valid_employee_kwargs())
        with pytest.raises(TypeError,match="parent department must be a department"):
            dep1.set_parent_department(emp1)
    def test_id_checked_for_validity(self):
        with patch("employee_tracker.domain.department.check_id", return_value="dep") as mock_check_id:
            dep1 = Department(**valid_department_kwargs())
            dep2 = Department(**valid_department_kwargs())
            dep1.set_parent_department(dep2)
            mock_check_id.assert_called_once_with(dep2.id,"dep")
    def test_rejects_invalid_id(self):
        dep1 = Department(**valid_department_kwargs())
        dep2 = Department(**valid_department_kwargs())
        dep2.id = "BadID"
        with pytest.raises(ValueError,match="invalid ID"):
             dep1.set_parent_department(dep2)
class TestRemoveParentDepartment:
    def test_department_has_remove_parent_department_method(self):
        assert hasattr(Department,"remove_parent_department")
    def test_remove_parent_department_removes_parent_department(self):
        dep1 = Department(**valid_department_kwargs())
        dep2 = Department(**valid_department_kwargs())
        dep1.set_parent_department(dep2)
        dep1.remove_parent_department()
        assert dep1.parent_department == None
    def test_raises_error_when_no_parent_department(self):
        dep1 = Department(**valid_department_kwargs())
        dep1.remove_parent_department()
        with pytest.raises(ValueError,match=f"{dep1.name} has no parent department to remove"):
            dep1.remove_parent_department()
