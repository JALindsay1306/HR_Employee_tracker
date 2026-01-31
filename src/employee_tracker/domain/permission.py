from employee_tracker.utils.ids import check_id

class Permission:
    def __init__(self,name,admin_id,departments = None):
        if not isinstance(name,str):
            raise TypeError("Name must be a string")
        if not check_id(admin_id,"emp"):
            raise TypeError("admin must be an employee")
        if (not isinstance(departments,list)) and (departments != None):
            raise TypeError("departments must be a dictionary")
        self.name = name
        self.admin_id = admin_id
        self.departments = departments
        if departments != None:
            for pair in departments:
                if not isinstance(pair, (list, tuple)) or len(pair) != 2:
                    raise TypeError("Incorrect format for department")

                dep_id, access = pair

                if not check_id(dep_id, "dep"):
                    raise TypeError(f"Department {dep_id} not found")

                if access not in ("read", "write", "full"):
                    raise TypeError("Invalid permission type")
        