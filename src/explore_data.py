import json
from pathlib import Path

import pandas as pd

data_folder = Path("data")


with open(data_folder / "input" / "example.json") as f:
    json_data = json.load(f)


df = pd.DataFrame(json_data.get("jobs"))

####

df.dtypes
df

## Wrangle time information  
# Adjust time stamps

df['first_import_at'] = pd.to_datetime(df['first_import_at'], unit='s')

df['last_seen_at'] = pd.to_datetime(df['last_seen_at'], unit='s')

df['expire_at'] = pd.to_datetime(df['expire_at'], unit='s')

# Adjust formatting


df