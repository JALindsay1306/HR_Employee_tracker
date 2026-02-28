from employee_tracker.utils.passwords import is_valid_stored_password_hash
from employee_tracker.utils.ids import check_id

# This class is used as part of the login process. In future updates this might be removed.
# The initial intention was to have this load before any other data, and other data not be loaded before login
# In practice, all data is loaded simultaneously in order to simplify load process
class User:
    def __init__(self,id,password_hash):
        if not is_valid_stored_password_hash(password_hash):
            raise ValueError("not a valid password hash")
        if not check_id(id,"emp"):
            raise ValueError("not a valid employee id")
        self._id = id
        self._password_hash = password_hash
    @property
    def id(self):
        return self._id
    @id.setter
    # id should not be changed, as it relates to an employee. This method protects against changes
    def id(self,new_id):
        raise ValueError("id cannot be altered")
    @property
    def password_hash(self):
        return self._password_hash
    @password_hash.setter
    def password_hash(self,new_password_hash):
        if not is_valid_stored_password_hash(new_password_hash):
            raise ValueError("not a valid password hash")
        self._password_hash = new_password_hash

    # method to prepare for storage
    def to_row(self):
        return {
            "id":self.id,
            "password_hash":self.password_hash,
        }
    
    # method to build a new class object from storage
    @classmethod
    def from_row(cls, row: dict) -> "User":
        
        return cls(
            id=row["id"],
            password_hash=row["password_hash"],
        )
    