from employee_tracker.utils.passwords import verify_password

# Login function that calls a utility for verifying passwords
def login(tracker: Tracker,emp_id: str,password_attempt: str) -> list:
    if emp_id not in tracker.users:
        raise LookupError("No such user")
    if verify_password(password_attempt,tracker.users[emp_id].password_hash):
        return tracker.employees[emp_id].permissions
    else:
        raise PermissionError("Incorrect password")
    