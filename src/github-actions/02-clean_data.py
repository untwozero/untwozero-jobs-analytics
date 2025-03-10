import ast
from http import HTTPStatus
from pathlib import Path

import pandas as pd
import requests

### Data ####

DATA_DIR = Path("data")
df = pd.read_csv(DATA_DIR / "public" / "raw_jobs_df.csv")

# df.dtypes
# df.columns
# len(df)

### Wrangling/Cleaning ###

# Set strict dtypes
df["url"] = df["url"].astype(str)
df["description"] = df["description"].astype(str)
df["is_homebased"] = df["is_homebased"].astype("boolean")


def extract_values(data, key="name"):
    if isinstance(data, str):
        try:
            data_literal = ast.literal_eval(data)
        except (ValueError, SyntaxError):
            return []

        if isinstance(data_literal, list):
            return [item.get(key, "") for item in data_literal]
        elif isinstance(data_literal, dict):
            return [
                v.get(key, "") if isinstance(v, dict) else ""
                for v in data_literal.values()
            ]
    return []


df["areas_clean"] = df["areas"].apply(extract_values)
df["levels_clean"] = df["levels"].apply(extract_values)


df["locations_names"] = df["locations"].apply(extract_values)


## Locations
# Example: [{'name': 'Addis Ababa', 'latitude': 9.0107934, 'longitude': 38.7612525}]
# can include multiple locations
# TODO: discuss how to deal with that in dashboard
df["locations_latitudes"] = df["locations"].apply(
    lambda x: extract_values(x, key="latitude")
)
df["locations_longitudes"] = df["locations"].apply(
    lambda x: extract_values(x, key="longitude")
)

## Company
df["company"] = df["company"].apply(ast.literal_eval)
df["company_name"] = df["company"].apply(
    lambda x: x.get("name", pd.NA) if isinstance(x, dict) else pd.NA
)
df["company_slug"] = df["company"].apply(
    lambda x: x.get("slug", pd.NA) if isinstance(x, dict) else pd.NA
)


df["expire_at"] = pd.to_datetime(df["expire_at"], errors="coerce")


## add redirect urls
df["url_apply"] = df["url"] + "/apply"
df["url_details"] = df["url"] + "/details"


## get org links
# FIXME: 404 Forbidden, probably does not allow on site
def get_redirect_url(url):
    try:
        response = requests.head(url, allow_redirects=True)
        if response.status_code == HTTPStatus.OK:
            return response.url
        else:
            return f"Error: {response.status_code} {HTTPStatus(response.status_code).phrase}"
    except requests.RequestException as e:
        return f"Request failed: {e}"


# df["redirect_url_apply"] = df["url_apply"].apply(get_redirect_url)
# df["redirect_url_details"] = df["url_details"].apply(get_redirect_url)


#### Export ####

df.to_csv(DATA_DIR / "public" / "clean_jobs_df.csv", index=False)
df.to_pickle(DATA_DIR / "public" / "clean_jobs_df.pkl")
