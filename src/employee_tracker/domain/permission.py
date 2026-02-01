from employee_tracker.domain.department import Department

class Permission:
    def __init__(self,name,department = None):
        if not isinstance(name,str):
            raise TypeError("Name must be a string")
        if (not isinstance(department,Department)) and (department != None):
            raise TypeError("department must be a valid department or all")
        self.name = name
        self.department = department