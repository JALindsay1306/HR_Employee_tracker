import pytest
from datetime import date
import time

from employee_tracker.data import employees_csv, departments_csv, permissions_csv
from employee_tracker.utils.generate_sample_data import generate_sample_data
from employee_tracker.domain.tracker import Tracker

def test_generate_returns_tracker():
    assert isinstance(generate_sample_data(),Tracker)
def test_returned_tracker_has_contents():
    trk = generate_sample_data()

    assert len(trk.departments) > 0 and len(trk.employees) > 0 and len(trk.permissions) > 0

def test_generate_writes_csv_files():
    paths = [employees_csv, departments_csv, permissions_csv]

    before = {p: (p.stat().st_mtime_ns if p.exists() else None) for p in paths}

    time.sleep(0.01)

    generate_sample_data()

    for p in paths:
        assert p.exists(), f"{p} was not created"
        after = p.stat().st_mtime_ns
        if before[p] is not None:
            assert after > before[p], f"{p} was not rewritten (mtime did not increase)"

