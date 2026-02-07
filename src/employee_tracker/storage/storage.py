import pandas as pd

def create_dataframe(data):
    return pd.DataFrame([{
        "id":data.id,
        "name":data.name,
        "role":data.role,
        "start_date":data.start_date,
        "salary":data.salary,
        "address":data.address,
        "permissions":data.permissions
    }])