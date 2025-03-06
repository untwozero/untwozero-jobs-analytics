"""
Fetching jobs from https://untalent.org/jobs via API

API Docs: https://github.com/UNTalent/Documentation

Other filter params:
 – levelSlugs
 – areaSlugs
 – locationSlugs
"""

import os
from pathlib import Path
from datetime import datetime, timedelta
import time

import pandas as pd
import requests
from dotenv import load_dotenv
import requests_cache


data_folder = Path("data")
db_path = data_folder / "database" / "api_cache.sqlite"

# Set up an API cache
requests_cache.install_cache(
    str(db_path),
    backend="sqlite",
    expire_after=timedelta(hours=1),
)


# Fetch all jobs (Pagination)
def fetch_all_jobs(api_token, starting_page=1):
    base_url = "https://untalent.org/api/v1/jobs"
    page = starting_page
    all_jobs = []

    while True:
        params = {"token": api_token, "page": page}

        try:
            resp = requests.get(base_url, params=params, timeout=20)
            resp.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx

        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            break

        print(f"Fetching page {page} - Status Code: {resp.status_code}")
        data = resp.json()
        jobs_on_page = data.get("jobs", [])

        if not jobs_on_page:
            print(f"No more jobs on page {page}. Stopping fetch.")
            break  # No more jobs available

        all_jobs.extend(jobs_on_page)
        page += 1

        ## Rate limiting
        # time.sleep(1)

    print(f"Total jobs fetched: {len(all_jobs)}")
    return all_jobs


####################################################################################

load_dotenv()

API_TOKEN = os.getenv("UNTALENT_API_TOKEN")
if not API_TOKEN:
    raise ValueError("No 'UNTALENT_API_TOKEN' found in /.env")


print("Fetching all jobs...")
all_jobs = fetch_all_jobs(API_TOKEN)
total_fetched = len(all_jobs)

jobs_df = pd.DataFrame(all_jobs)
jobs_df

### Export ###

data_folder = Path("data")

output_folder = data_folder / "output"
output_folder.mkdir(parents=True, exist_ok=True)

jobs_df.to_csv(output_folder / "raw_jobs_df.csv", index=False)
jobs_df.to_pickle(output_folder / "raw_jobs_df.pkl")
