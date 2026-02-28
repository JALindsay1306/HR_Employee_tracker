from employee_tracker.domain.department import Department
from employee_tracker.utils.ids import check_id


# Currently this class is under-utilised. Permission names are hard coded in the GUI level
# The intention of keeping this class is that there may be new ones added in future
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
    # "Active" was originally meant to be used as part of permission validation at class-level
    # However, permissions were then moved to be within a list at the upper "tracker" level
    # As such Active is current not used, but kept here to be part of future plans
    @property
    def active(self):
        return self._active
    @active.setter
    def active(self,activate):
        if not isinstance(activate,bool):
            raise TypeError("active must be a boolean value")
        self._active = activate
    
    # Quick storage preparation
    def to_row(self):
        return {
            "name":self.name,
            "active":self.active 
        }
    # Given there is no automatic ID creation, this doesn't strictly need to be a class method
    # However, it was kept this way for homogeneity with Employee and Department
    @classmethod
    def from_row(cls, row: dict) -> "Permission":
        active = False
        if "active" in row:
            active = row["active"]
        return cls(
            name=row["name"],
            active=active
        )
