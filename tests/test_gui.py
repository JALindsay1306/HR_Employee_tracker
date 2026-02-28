import os
import pytest
import tkinter as tk
from datetime import date
from types import SimpleNamespace
from unittest.mock import MagicMock

def _tk_available() -> bool:
    try:
        r = tk.Tk()
        r.withdraw()
        r.destroy()
        return True
    except Exception:
        return False

TK_AVAILABLE = _tk_available()

skip_if_no_tk = pytest.mark.skipif(
    not TK_AVAILABLE,
    reason="Tk/Tcl runtime not available (init.tcl missing). Install a Python build with Tk support (python.org) or run GUI tests under Xvfb."
)

HEADLESS_LINUX = (os.name != "nt") and (os.environ.get("DISPLAY") is None)
pytestmark = pytest.mark.skipif(
    HEADLESS_LINUX,
    reason="Tkinter GUI tests require a display (no $DISPLAY set)."
)


@pytest.fixture
def tk_root():
    root = tk.Tk()
    root.withdraw()
    yield root
    try:
        root.destroy()
    except tk.TclError:
        pass


class TestGUIFunctions:
    def test_parse_employee_form_ok(self):
        from employee_tracker.gui.employee_window import parse_employee_form

        data = parse_employee_form("Alice", "Engineer", "2024-01-15", "90000", "123 Road")
        assert data["name"] == "Alice"
        assert data["role"] == "Engineer"
        assert data["start_date"] == date(2024, 1, 15)
        assert data["salary"] == 90000
        assert data["address"] == "123 Road"

    @pytest.mark.parametrize("bad_date", ["2024/01/01", "not-a-date", "2024-13-01", ""])
    def test_parse_employee_form_bad_date(self, bad_date):
        from employee_tracker.gui.employee_window import parse_employee_form

        with pytest.raises(ValueError, match="Start date must be YYYY-MM-DD"):
            parse_employee_form("A", "R", bad_date, "10", "X")

    @pytest.mark.parametrize("bad_salary", ["10.5", "abc", ""])
    def test_parse_employee_form_bad_salary(self, bad_salary):
        from employee_tracker.gui.employee_window import parse_employee_form

        with pytest.raises(ValueError, match="Salary must be an integer"):
            parse_employee_form("A", "R", "2024-01-01", bad_salary, "10 Downing St")

    def test_parse_department_form_ok(self, monkeypatch):
        import employee_tracker.gui.department_window as dw

        monkeypatch.setattr(dw, "check_id", lambda value, kind: True)

        data = dw.parse_department_form("IT", "Tech", "emp_12345678", "dep_12345678")
        assert data["name"] == "IT"
        assert data["description"] == "Tech"
        assert data["head_of_department"] == "emp_12345678"
        assert data["parent_department"] == "dep_12345678"

    def test_parse_department_form_rejects_bad_head_id(self, monkeypatch):
        import employee_tracker.gui.department_window as dw

        monkeypatch.setattr(dw, "check_id", lambda value, kind: False)
        with pytest.raises(ValueError, match="Head of department must be an employee ID"):
            dw.parse_department_form("IT", "Tech", "bad", "")


class TestLoginWindow:
    def test_login_window_success_callback_and_closes(self, tk_root, monkeypatch):
        from employee_tracker.gui.login_window import LoginWindow

        tracker = MagicMock()
        called = {}

        def on_success(perms, emp_id):
            called["perms"] = perms
            called["emp_id"] = emp_id

        monkeypatch.setattr(
            "employee_tracker.gui.login_window.login",
            lambda tr, emp, pw: ["it_admin"]
        )

        win = LoginWindow(tk_root, tracker, on_success)
        win.withdraw()
        try:
            win.emp_id_var.set("emp_12345678")
            win.password_var.set("pw")
            win.do_login()

            assert called["emp_id"] == "emp_12345678"
            assert called["perms"] == ["it_admin"]
            assert not win.winfo_exists()
        finally:
            if win.winfo_exists():
                win.destroy()

    def test_login_window_failure_shows_error(self, tk_root, monkeypatch):
        from employee_tracker.gui.login_window import LoginWindow

        tracker = MagicMock()
        called = {"success": False}

        def on_success(perms, emp_id):
            called["success"] = True

        def bad_login(tr, emp, pw):
            raise LookupError("No such user")

        monkeypatch.setattr("employee_tracker.gui.login_window.login", bad_login)

        showerror = MagicMock()
        monkeypatch.setattr("employee_tracker.gui.login_window.messagebox.showerror", showerror)

        win = LoginWindow(tk_root, tracker, on_success)
        win.withdraw()
        try:
            win.emp_id_var.set("emp9999")
            win.password_var.set("pw")
            win.do_login()

            assert called["success"] is False
            showerror.assert_called()
            assert win.winfo_exists()
        finally:
            if win.winfo_exists():
                win.destroy()


class TestMainWindow:
    def test_mainwindow_on_login_success_updates_status(self, monkeypatch):
        from employee_tracker.gui import main_window as mw

        monkeypatch.setattr(mw.MainWindow, "show_login", lambda self: None)

        tracker = MagicMock()
        app = mw.MainWindow(tracker)
        app.root.withdraw()
        try:
            app.on_login_success(["it_admin"], "emp_12345678")

            assert "emp_12345678" in app.root.title()
            assert "it_admin" in app.status_var.get()

            assert str(app.btn_employees["state"]) == "normal"
            assert str(app.btn_departments["state"]) == "normal"
        finally:
            try:
                app.root.destroy()
            except tk.TclError:
                pass


class TestEmployeeWindow:
    class FakePasswordDialog:
        def __init__(self, *args, **kwargs):
            pass

        def show(self):
            return "secret"

    @staticmethod
    def make_fake_employee(emp_id="emp_12345678"):
        return SimpleNamespace(
            id=emp_id,
            name="Alice",
            role="Engineer",
            start_date=date(2024, 1, 15),
            salary=50000,
            address="123 Road",
            password_hash="hash",
        )

    def test_employee_create_denied_shows_error(self, tk_root, monkeypatch):
        from employee_tracker.gui.employee_window import EmployeeWindow

        tracker = MagicMock()
        tracker.list_employees.return_value = []

        showerror = MagicMock()
        monkeypatch.setattr("employee_tracker.gui.employee_window.messagebox.showerror", showerror)

        win = EmployeeWindow(tk_root, tracker, permissions=[], logged_in_user=None)
        win.withdraw()
        try:
            win.on_create()
            showerror.assert_called()
            assert tracker.create_employee.called is False
        finally:
            win.destroy()

    def test_employee_create_success_calls_tracker(self, tk_root, monkeypatch):
        from employee_tracker.gui.employee_window import EmployeeWindow

        tracker = MagicMock()
        tracker.list_employees.return_value = []
        tracker.create_employee.return_value = SimpleNamespace(id="emp_99999999")

        monkeypatch.setattr("employee_tracker.gui.employee_window.PasswordDialog", self.FakePasswordDialog)
        monkeypatch.setattr("employee_tracker.gui.employee_window.messagebox.showerror", MagicMock())

        win = EmployeeWindow(tk_root, tracker, permissions=["hr_write"], logged_in_user="emp_23456789")
        win.withdraw()
        try:
            win.name_entry.delete(0, "end"); win.name_entry.insert(0, "Bob")
            win.role_entry.delete(0, "end"); win.role_entry.insert(0, "Analyst")
            win.start_date_entry.delete(0, "end"); win.start_date_entry.insert(0, "2024-02-01")
            win.salary_entry.delete(0, "end"); win.salary_entry.insert(0, "60000")
            win.address_entry.delete(0, "end"); win.address_entry.insert(0, "Street 9")

            win.on_create()

            tracker.create_employee.assert_called_once()
            _, kwargs = tracker.create_employee.call_args
            assert kwargs["password"] == "secret"
            assert kwargs["name"] == "Bob"
            assert kwargs["role"] == "Analyst"
            assert kwargs["start_date"] == date(2024, 2, 1)
            assert kwargs["salary"] == 60000
            assert kwargs["address"] == "Street 9"
        finally:
            win.destroy()

class TestDepartmentWindow:
    @staticmethod
    def make_fake_department(dep_id="dep_12345678"):
        return SimpleNamespace(
            id=dep_id,
            name="IT",
            description="Tech",
            head_of_department="emp_12345678",
            parent_department=None,
            members=["emp_12345678"],
            remove_employee=MagicMock(),
        )

    def test_department_update_changes_description_not_name(self, tk_root, monkeypatch):
        from employee_tracker.gui.department_window import DepartmentWindow
        import employee_tracker.gui.department_window as dw

        monkeypatch.setattr(dw, "check_id", lambda value, kind: True)
        monkeypatch.setattr("employee_tracker.gui.department_window.messagebox.showerror", MagicMock())

        dep = self.make_fake_department("dep_12345678")

        tracker = MagicMock()
        tracker.list_departments.return_value = [dep]
        tracker.departments = {"dep_12345678": dep}
    
        tracker.employees = {"emp_12345678": TestEmployeeWindow.make_fake_employee("emp_12345678")}

        win = DepartmentWindow(tk_root, tracker, permissions=["hr_write"], logged_in_user="emp_12345678")
        win.withdraw()
        try:
            win.selected_department_id = "dep_12345678"

            win.name_entry.delete(0, "end"); win.name_entry.insert(0, "IT")
            win.description_entry.delete(0, "end"); win.description_entry.insert(0, "New Desc")
            win.head_of_department_entry.delete(0, "end"); win.head_of_department_entry.insert(0, "emp_12345678")
            win.parent_department_entry.delete(0, "end"); win.parent_department_entry.insert(0, "")

            win.on_update()

            assert dep.name == "IT"
            assert dep.description == "New Desc"
        finally:
            win.destroy()

    def test_department_add_members_denied_without_perms(self, tk_root, monkeypatch):
        from employee_tracker.gui.department_window import DepartmentWindow
        import employee_tracker.gui.department_window as dw

        monkeypatch.setattr(dw, "check_id", lambda value, kind: True)

        dep = self.make_fake_department("dep_12345678")
        tracker = MagicMock()
        tracker.list_departments.return_value = [dep]
        tracker.departments = {"dep_12345678": dep}

        showerror = MagicMock()
        monkeypatch.setattr("employee_tracker.gui.department_window.messagebox.showerror", showerror)

        win = DepartmentWindow(tk_root, tracker, permissions=[], logged_in_user="emp_99999999")
        win.withdraw()
        try:
            win.selected_department_id = "dep_12345678"
            win.open_add_members_window()
            showerror.assert_called()
        finally:
            win.destroy()

@skip_if_no_tk
class TestAddMembersWindow:
    def test_add_members_window_filters_out_existing_members(self, tk_root):
        from employee_tracker.gui.add_members_window import AddMembersWindow

        emp1 = TestEmployeeWindow.make_fake_employee("emp_11112222")
        emp2 = TestEmployeeWindow.make_fake_employee("emp_22223333")
        dep = SimpleNamespace(id="dep_12345678", members=["emp_11112222"])

        tracker = SimpleNamespace(
            departments={"dep_12345678": dep},
            list_employees=lambda: [emp1, emp2],
            add_employee_to_department=MagicMock(),
        )

        win = AddMembersWindow(tk_root, tracker, "dep_12345678")
        win.withdraw()
        try:
            win.refresh_employee_list()
            assert "emp_11112222" not in win.emp_ids
            assert "emp_22223333" in win.emp_ids
        finally:
            win.destroy()

    def test_add_members_window_add_selected_calls_tracker(self, tk_root, monkeypatch):
        from employee_tracker.gui.add_members_window import AddMembersWindow

        emp1 = TestEmployeeWindow.make_fake_employee("emp_11112222")
        emp2 = TestEmployeeWindow.make_fake_employee("emp_22223333")
        dep = SimpleNamespace(id="dep_12345678", members=[])

        tracker = SimpleNamespace(
            departments={"dep_12345678": dep},
            list_employees=lambda: [emp1, emp2],
            add_employee_to_department=MagicMock(),
        )

        monkeypatch.setattr("employee_tracker.gui.add_members_window.messagebox.showinfo", MagicMock())
        monkeypatch.setattr("employee_tracker.gui.add_members_window.messagebox.showerror", MagicMock())

        win = AddMembersWindow(tk_root, tracker, "dep_12345678")
        win.withdraw()
        try:
            win.emp_listbox.selection_set(0)
            win.on_add_selected()
            tracker.add_employee_to_department.assert_called_once()
        finally:
            win.destroy()