import pytest
from datetime import date
from employee_tracker.utils.ids import new_id, check_id
from employee_tracker.utils.value_checkers import check_new_value
from employee_tracker.utils.filtering import filter_list
from employee_tracker.domain.employee import Employee

def valid_employee_kwargs():
    return dict(
        name="James",
        role="Creator",
        start_date=date(2024, 10, 2),
        salary=30000,
        address="123 Lane, Town, County",
    )

class TestIDCreation:
    def test_id_prefix_used(self):
        result = new_id("idtest")
        assert result.startswith("idtest")
    def test_id_suffix_characters_are_hex(self):
        result = new_id("id")
        suffix = result.split("_")[1]
        assert isinstance(int(suffix,16),int)
    def test_id_has_8_hex_chars(self):
        result = new_id("id")
        suffix = result.split("_")[1]
        assert len(suffix) == 8
    def test_ids_created_are_unique(self):
        id_1 = new_id("id")
        id_2 = new_id("id")
        id_3 = new_id("id")
        id_4 = new_id("id")

        assert id_1 != id_2 and id_1 != id_3 and id_1 != id_4 and id_2 != id_3 and id_2 != id_4 and id_3 != id_4 

class TestIDChecker:
    def test_correct_id_passes(self):
        id = new_id("test")
        assert check_id(id,"test") is True
    def test_wrong_prefix_fails(self):
        id = new_id("test")
        assert check_id(id,"test2") is False
    def test_too_short_fails(self):
        id = new_id("test")
        id_split = id.split("_")
        id_split[1] = id_split[1][0:5]
        id = "_".join(id_split)
        assert check_id(id,"test") is False
    def test_too_long_fails(self):
        id = new_id("test")
        id_split = id.split("_")
        id_split[1] = id_split[1]+"88"
        id = "_".join(id_split)
        assert check_id(id,"test") is False
    def test_nonhex_fails(self):
        id = new_id("test")
        id_split = id.split("_")
        suffix = id_split[1]
        id_split[1] = suffix[0:2] + "Z" + suffix[3:]
        id = "_".join(id_split)
        assert check_id(id,"test") is False

class TestCheckNewValue:
    def test_correct_new_value_passes(self):
        assert check_new_value("Jim","name",str,"John")
    def test_wrong_type_fails(self):
        with pytest.raises(TypeError, match = "name must be a <class 'str'>"):
            check_new_value(123,"name",str)
    def test_duplicate_value_fails(self):
        with pytest.raises(ValueError, match = "New salary must be different to existing salary"):
            check_new_value(50000,"salary",int,50000)

class TestFiltering:
    def test_filter_list_returns_a_list_of_class_objects_when_passed_one(self):
        emp_list = [
            Employee(**valid_employee_kwargs()),
            Employee(**valid_employee_kwargs()),
            Employee(**valid_employee_kwargs()),
            Employee(**valid_employee_kwargs())
        ]
        filtered_list = filter_list(emp_list,"name","James","string")
        assert isinstance(filtered_list,list)
        assert len(filtered_list)
        for employee in filtered_list:
            assert hasattr(employee,"id")
            assert hasattr(employee,"name")
            assert hasattr(employee,"role")
            assert hasattr(employee,"start_date")
    def test_filter_filters_by_one_parameter(self):
        emp_list = [
            Employee(**valid_employee_kwargs()),
            Employee(**valid_employee_kwargs()),
            Employee(**valid_employee_kwargs()),
            Employee(**valid_employee_kwargs())
        ]
        emp_list[0].name = "SSSteve"
        emp_list[1].name = "SSSharon"
        filtered_list = filter_list(emp_list,"name","SSS")
        assert len(filtered_list) == 2
        assert filtered_list[0].name == "SSSteve" and filtered_list[1].name == "SSSharon"
    def test_filter_on_min_values(self):
        emp_list = [
            Employee(**valid_employee_kwargs()),
            Employee(**valid_employee_kwargs()),
            Employee(**valid_employee_kwargs()),
            Employee(**valid_employee_kwargs())
        ]
        emp_list[0].salary = 50000
        emp_list[1].salary = 60000
        emp_list[2].salary = 80000
        emp_list[3].salary = 90000
        filtered_list = filter_list(emp_list,"salary",70000,"min")
        assert len(filtered_list) == 2
        assert filtered_list[0].salary == 80000 and filtered_list[1].salary == 90000
    def test_filter_on_max_values(self):
        emp_list = [
            Employee(**valid_employee_kwargs()),
            Employee(**valid_employee_kwargs()),
            Employee(**valid_employee_kwargs()),
            Employee(**valid_employee_kwargs())
        ]
        emp_list[0].salary = 50000
        emp_list[1].salary = 60000
        emp_list[2].salary = 80000
        emp_list[3].salary = 90000
        filtered_list = filter_list(emp_list,"salary",70000,"max")
        assert len(filtered_list) == 2
        assert filtered_list[0].salary == 50000 and filtered_list[1].salary == 60000
    def test_filter_validates_strings(self):
        emp_list = [
            Employee(**valid_employee_kwargs()),
            Employee(**valid_employee_kwargs()),
            Employee(**valid_employee_kwargs()),
            Employee(**valid_employee_kwargs())
        ]
        with pytest.raises(TypeError,match="String expected, please try again"):
            filtered_list = filter_list(emp_list,"role",70000)
    def test_filter_validates_max_and_min_ints(self):
        emp_list = [
            Employee(**valid_employee_kwargs()),
            Employee(**valid_employee_kwargs()),
            Employee(**valid_employee_kwargs()),
            Employee(**valid_employee_kwargs())
        ]
        with pytest.raises(TypeError,match="Integer or date expected, please try again"):
            filtered_list = filter_list(emp_list,"salary","Lots","max")
    def test_filter_validates_max_and_min_dates(self):
        emp_list = [
            Employee(**valid_employee_kwargs()),
            Employee(**valid_employee_kwargs()),
            Employee(**valid_employee_kwargs()),
            Employee(**valid_employee_kwargs())
        ]
        with pytest.raises(TypeError,match="Integer or date expected, please try again"):
            filtered_list = filter_list(emp_list,"start_date",True,"min")
    def test_filter_does_not_accept_incorrect_types(self):
         emp_list = [
            Employee(**valid_employee_kwargs()),
            Employee(**valid_employee_kwargs()),
            Employee(**valid_employee_kwargs()),
            Employee(**valid_employee_kwargs())
        ]
         with pytest.raises(TypeError,match="Parameter type should be string, max or min"):
            filtered_list = filter_list(emp_list,"salary",45000,"money")
    
        