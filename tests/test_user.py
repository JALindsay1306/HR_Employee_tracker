import pytest

from employee_tracker.domain.user import User
from employee_tracker.utils.passwords import hash_password, verify_password,is_valid_stored_password_hash

def valid_user_kwargs():
    hash = hash_password("password")
    return dict(
        id = "emp_12345678",
        password_hash = hash
    )

class TestUserCreation:
    def test_user_can_be_created(self):
        user = User(**valid_user_kwargs())
        assert isinstance(user,User)
        assert hasattr(user,"id")
        assert hasattr(user,"password_hash")

class TestUserParameterValidation:
     @pytest.mark.parametrize(
        "field,value,error",
        [
            ("id", 123, "not a valid employee id"),
            ("password_hash", "bad_hash", "not a valid password hash"),
        ],
     )
     def test_invalid_datatypes(self, field, value, error):
        kwargs = valid_user_kwargs()
        kwargs[field] = value

        with pytest.raises(ValueError, match=error):
            User(**kwargs)

class TestIDProtection:
    def test_id_cannot_be_changed(self):
        user = User(**valid_user_kwargs())
        with pytest.raises(ValueError,match="id cannot be altered"):
            user.id = "emp_87652738"

class TestPasswordUpdate:
    def test_password_hash_can_be_updated(self):
        user = User(**valid_user_kwargs())
        new_hash = hash_password("new")
        user.password_hash = new_hash
        assert user.password_hash == new_hash
        assert is_valid_stored_password_hash(user.password_hash)
    def test_cannot_update_with_invalid_hash(self):
        user = User(**valid_user_kwargs())
        new_hash = "bad_hash"
        with pytest.raises(ValueError,match="not a valid password hash"):
            user.password_hash = new_hash