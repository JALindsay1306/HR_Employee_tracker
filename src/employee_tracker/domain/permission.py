from employee_tracker.domain.department import Department

class Permission:
    def __init__(self,name,department = None):
        if not isinstance(name,str):
            raise TypeError("Name must be a string")
        if (not isinstance(department,str)) and (department != None):
            raise TypeError("department must be a str")
        self.name = name
        self.department = department
    def change_name(self,new_name):
        pass
    def list_departments(self):
        pass
    def add_departments(self):
        pass
    def remove_department(self):
        pass
    def wipe_departments(self):
        pass