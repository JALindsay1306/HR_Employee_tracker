import uuid

def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

print (new_id("ID"))

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