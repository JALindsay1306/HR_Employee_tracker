from employee_tracker.domain.department import Department
from employee_tracker.utils.ids import check_id

class Permission:
    def __init__(self,name,active = False):
        if not isinstance(name,str):
            raise TypeError("Name must be a string")
        if (not isinstance(active,bool)):
            raise TypeError("active must be a boolean value")
        self._name = name
        self._active = active
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,new_name):
        if not isinstance(new_name,str):
            raise TypeError("name must be a string")
        elif new_name == self.name:
            raise ValueError(f"name is already {new_name}")
        self._name = new_name
    @property
    def active(self):
        return self._active
    @active.setter
    def active(self,activate):
        if not isinstance(activate,bool):
            raise TypeError("active must be a boolean value")
        self._active = activate
    
    def to_row(self):
        return {
            "name":self.name,
            "active":self.active 
        }
    @classmethod
    def from_row(cls, row: dict) -> "Permission":
        active = False
        if "active" in row:
            active = row["active"]
        return cls(
            name=row["name"],
            active=active
        )
