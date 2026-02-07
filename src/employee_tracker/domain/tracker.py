from employee_tracker.domain.employee import Employee
from employee_tracker.domain.department import Department
from employee_tracker.domain.permission import Permission
from employee_tracker.utils.ids import check_id
from employee_tracker.utils.filtering import filter_list

class Tracker:
    def __init__(self):
        self.employees = {}
        self.departments = {}
        self.permissions = {}
    def create_employee(self,name,role, start_date,salary,address,permissions = None):
        if permissions != None:
            if not isinstance(permissions,list):
                raise TypeError("permissions must be a list of permission ids")
            else:
                for permission in permissions:
                    if not check_id(permission,"per"):
                        raise TypeError("permissions in list must be valid permission ids")
        emp = Employee(name,role,start_date,salary,address,permissions)
        self.employees[emp.id] = emp
        return emp
    def list_employees(self,name_search=None,role_search=None,min_date=None,max_date=None,min_salary=None,max_salary=None,permissions=None):
        employee_list = list(self.employees.values())
        for key,value in {name_search:["name","string"],role_search:["role","string"],min_date:["start_date","min"],max_date:["start_date","max"],min_salary:["salary","min"],max_salary:["salary","max"]}.items():
            if key !=None:
                employee_list = filter_list(employee_list,value[0],key,value[1])   
        return employee_list
    def create_department(self,name,description,head_of_department,parent_department=None,members=None):
        if not check_id(head_of_department,"emp"):
            raise TypeError("head_of_department must be a valid employee id")
        if parent_department != None:
            if not check_id(parent_department,"dep"):
                raise TypeError("parent_department must be a valid department id")
        if members != None:
            if not isinstance(members,list):
                raise TypeError("members must be a list of employee ids")
            else:
                for employee in members:
                    if not check_id(employee,"emp"):
                        raise TypeError("members in list must be valid employee ids")
        dep = Department(name,description,head_of_department,parent_department,members)
        self.departments[dep.id] = dep
        return dep
    def create_permission(self,name,department = None):
        if department != None and not check_id(department,"dep"):
            raise TypeError("department must be a valid department id")
        per = Permission(name,department)
        self.permissions[per.name] = per
        return per