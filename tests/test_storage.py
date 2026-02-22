import pytest
import pandas as pd
from datetime import date
from datetime import date
from pandas.testing import assert_frame_equal

from employee_tracker.domain.tracker import Tracker
from employee_tracker.domain.employee import Employee
from employee_tracker.domain.department import Department
from employee_tracker.domain.permission import Permission
from employee_tracker.storage.storage import create_dataframe
from employee_tracker.storage.storage import write_csv
from employee_tracker.storage.storage import read_csv

def valid_employee_kwargs():
    return dict(
        name="James",
        role="Creator",
        start_date=date(2024, 10, 2),
        salary=30000,
        address="123 Lane, Town, County",
        password_hash="zXl7n7B2cF9ZzC6bX5mJ8sQ2k1pLr4vTtYw9aBcDeFgHiJkLmNoPqRsTuVwXyZ12"
    )

def valid_department_kwargs(dep_name,head,parent=None):
    return dict(
        name=dep_name,
        description = "It's where the money is",
        head_of_department = head,
        parent_department = parent
    )


def example_tracker_creation():
    #create Tracker
    trk = Tracker()

    #create Employees
    emp_1 = trk.create_employee(**valid_employee_kwargs())
    emp_2 = trk.create_employee(**valid_employee_kwargs())
    emp_3 = trk.create_employee(**valid_employee_kwargs())
    emp_4 = trk.create_employee(**valid_employee_kwargs())
    emp_5 = trk.create_employee(**valid_employee_kwargs())
    emp_6 = trk.create_employee(**valid_employee_kwargs())
    emp_7 = trk.create_employee(**valid_employee_kwargs())
    emp_8 = trk.create_employee(**valid_employee_kwargs())
    emp_9 = trk.create_employee(**valid_employee_kwargs())

    dep_2 = trk.create_department(**valid_department_kwargs("IT",emp_2.id))
    dep_1 = trk.create_department(**valid_department_kwargs("Finance",emp_1.id,dep_2.id))    
    dep_4 = trk.create_department(**valid_department_kwargs("HR",emp_4.id,dep_2.id))
    dep_3 = trk.create_department(**valid_department_kwargs("Shipping",emp_3.id,dep_4.id))
    
   
    trk.departments[dep_1.id].add_employee(trk.employees[emp_5.id])
    trk.departments[dep_2.id].add_employee(trk.employees[emp_6.id])
    trk.departments[dep_3.id].add_employee(trk.employees[emp_7.id])
    trk.departments[dep_3.id].add_employee(trk.employees[emp_8.id])
    trk.departments[dep_4.id].add_employee(trk.employees[emp_9.id])

    return trk

class TestDataFrameCreation:
    def test_create_dataframe_returns_dataframe(self):
        trk = example_tracker_creation()
        df_trk_emps = create_dataframe(trk.list_employees())
        
        assert isinstance(df_trk_emps, pd.DataFrame)
        assert len(df_trk_emps) == 9
        assert set(["id", "name", "role", "start_date", "salary", "address", "permissions"]).issubset(df_trk_emps.columns)
    def test_error_handling_for_no_data(self):
        trk = Tracker()
        with pytest.raises(ValueError,match="No data to save, please check"):
            create_dataframe(trk.list_employees())

class TestCSVManagement:
    def test_round_trip_save_and_read_df(self):

        original = create_dataframe(example_tracker_creation().list_employees())
        original["start_date"] = pd.to_datetime(original["start_date"])
        
        write_csv("employees", original)
        loaded = read_csv("employees")

        loaded = loaded[original.columns]

        assert_frame_equal(loaded, original, check_dtype=False) 