HR Employee Tracker

A desktop HR management application built with Python and Tkinter.
The system supports employee and department management, login authentication, permission-based access control, and CSV data persistence.

Features

Secure login with hashed passwords (PBKDF2-HMAC-SHA256)

Employee management (create, update, delete)

Department management (create, update, delete, manage members)

Role-based permissions (e.g. HR, Payroll, IT Admin)

CSV-based data storage

Automatic sample data generation on first run

Comprehensive pytest test suite

Requirements

Python 3.10+

pandas

pytest (for running tests)

Install dependencies:

pip install pandas pytest
Running the Application

From the project root:

python -m employee_tracker.gui.main_window

On first run, if no CSV files exist, sample data will be generated automatically.

Running Tests

From the project root:

pytest

For verbose output:

pytest -vv
Notes

Data is stored in employee_tracker/data/ as CSV files.

Passwords are never stored in plaintext.

Permissions control what users can view and edit within the GUI.