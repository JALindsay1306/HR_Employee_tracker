import pytest
import pandas as pd
from datetime import date

from employee_tracker.domain.tracker import Tracker
from employee_tracker.domain.employee import Employee
from employee_tracker.domain.department import Department
from employee_tracker.domain.permission import Permission
from employee_tracker.storage.storage import create_dataframe

def valid_employee_kwargs():
    return dict(
        name="James",
        role="Creator",
        start_date=date(2024, 10, 2),
        salary=30000,
        address="123 Lane, Town, County",
    )

class TestDataFrameCreation:
    def test_dataframe_returned(self):
        emp1 = Employee(**valid_employee_kwargs())
        emp1df = create_dataframe(emp1)
        assert isinstance (emp1df,pd.DataFrame)
    