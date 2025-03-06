import os
import pandas as pd
import requests
from pathlib import Path

# Get API Token directly from GitHub Secrets (Environment Variable)
API_TOKEN = os.environ.get("UNTALENT_API_TOKEN")
if not API_TOKEN:
    raise ValueError(
        "No API Token found. Make sure UNTALENT_API_TOKEN is set in GitHub Secrets."
    )


## Define paths

print(f"Current working directory: {os.getcwd()}")
#> Current working directory: /home/runner/work/untwozero-jobs-analytics/untwozero-jobs-analytics

DATA_DIR = Path("data")
OUTPUT_DIR = DATA_DIR / "public"

# Ensure required directories exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def fetch_all_jobs(api_token, starting_page=0):
    """Fetch all jobs from the UNTALENT API with pagination."""
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

    print(f"Total jobs fetched: {len(all_jobs)}")
    return all_jobs


# Run the script
print("Fetching all jobs...")
all_jobs = fetch_all_jobs(API_TOKEN)

# Convert to DataFrame
jobs_df = pd.DataFrame(all_jobs)

### Export Data ###
csv_path = OUTPUT_DIR / "raw_jobs_df.csv"
jobs_df.to_csv(csv_path, index=False)

print(f"Jobs saved to {csv_path}")
#> Jobs saved to /home/runner/work/untwozero-jobs-analytics/untwozero-jobs-analytics/data/public/raw_jobs_df.csv
