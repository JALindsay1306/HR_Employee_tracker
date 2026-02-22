from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

employees_csv = DATA_DIR / "employees.csv"
departments_csv = DATA_DIR / "departments.csv"
permissions_csv = DATA_DIR / "permissions.csv"