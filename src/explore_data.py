import json
from pathlib import Path

import pandas as pd

data_folder = Path("data")


with open(data_folder / "input" / "example.json") as f:
    json_data = json.load(f)


df = pd.DataFrame(json_data.get("jobs"))

####

df.dtypes
