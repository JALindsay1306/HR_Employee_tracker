#simple function to check that a new value is the correct type and isn't overwriting itself

def check_new_value(new_value,variable,type, existing_value=None):
    if not isinstance(new_value,type):
            raise TypeError(f"{variable} must be a {type}")
    elif new_value == existing_value:
        raise ValueError(f"New {variable} must be different to existing {variable}")
    else:
        return True