import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def create_dataframe(dataset):
    if len(dataset) == 0:
        raise ValueError("No data to save, please check")
    rows = []
    for item in dataset:
        rows.append(item.to_row())
    
    return pd.DataFrame(rows)
 
def write_csv(file_type: str, dataframe):
    file_path = DATA_DIR / f"{file_type}.csv"
    dataframe.to_csv(file_path, index=False)

def read_csv(file_type: str) -> pd.DataFrame:
    file_path = DATA_DIR / f"{file_type}.csv"
    return pd.read_csv(
        file_path, 
        parse_dates=["start_date"],
        keep_default_na=False
    )