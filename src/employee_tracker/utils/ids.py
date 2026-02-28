import uuid

# Creates an id, with a passed prefix, followed by an underscore and an 8 digit hex number
def new_id(prefix: str) -> str:
    ### AI DECLARATION - the uuid usage was learned via ChatGPT, along with utilisation of "hex"
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


# checks that passed ID matches the correct pattern (both prefix and hex number)
def check_id(id,prefix):
    if not isinstance(id,str):
        return False
    if not id.startswith(prefix):
        return False
    elif not len(id.split("_")[1]) == 8:
        return False
    else:
        try:
            suffix = id.split("_")[1]
            if isinstance(int(suffix,16),int):
                return True
        except ValueError:
            return False