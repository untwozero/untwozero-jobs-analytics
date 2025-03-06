"""
Fetching jobs from https://untalent.org/jobs via API

API Docs: https://github.com/UNTalent/Documentation
"""

import os
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv


# Fetch all jobs (Pagination)
def fetch_all_jobs(api_token, starting_page=1):
    base_url = "https://untalent.org/api/v1/jobs"
    page = starting_page
    all_jobs = []

    ## other filter params:
    # – levelSlugs
    # – areaSlugs
    # – locationSlugs

    while True:
        params = {"token": api_token, "page": page}
        resp = requests.get(base_url, params=params)

        print(f"Fetching page {page} - Status Code: {resp.status_code}")

        if resp.status_code != 200:
            print(f"Error fetching page {page}: HTTP {resp.status_code}")
            break

        data = resp.json()
        jobs_on_page = data.get("jobs", [])

        if not jobs_on_page:
            print(f"No more jobs on page {page}. Stopping fetch.")
            break  # No more jobs available

        all_jobs.extend(jobs_on_page)
        page += 1

    print(f"Total jobs fetched: {len(all_jobs)}")
    return all_jobs


####################################################################################


load_dotenv()

API_TOKEN = os.getenv("UNTALENT_API_TOKEN")
if not API_TOKEN:
    raise ValueError("No 'UNTALENT_API_TOKEN' found in environment variables.")


print("Fetching all jobs...")
all_jobs = fetch_all_jobs(API_TOKEN)


total_fetched = len(all_jobs)
if total_fetched == 0:
    print("No jobs found or invalid token. Exiting.")


jobs_df = pd.DataFrame(all_jobs)
jobs_df

### Export ###

data_folder = Path("data")

jobs_df.to_csv(data_folder / "output" / "jobs_df.csv", index=False)
jobs_df.to_pickle(data_folder / "output" / "jobs_df.pkl")
