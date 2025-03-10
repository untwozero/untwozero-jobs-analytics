from pathlib import Path

import pandas as pd

### Data ####

DATA_DIR = Path("data")
# df = pd.read_csv(DATA_DIR / "public" / "clean_jobs_df.csv")

# this maintains list formatting

# TODO: read in analysis file
# df = pd.read_pickle(DATA_DIR / "output" / "clean_jobs_df.pkl")

# df = pd.read_pickle(DATA_DIR / "public" / "clean_jobs_df.pkl")
# df.dtypes


############################################################################################

## Example
# 1️⃣ Deputy Executive Secretary for Strategy, Innovation & Partnerships | United Nations Economic and Social Commission for Western Asia (ESCWA), hashtag#Beirut, D2 | 17 Apr https://lnkd.in/e6S6tkCy


def create_job_posting(row):
    # Format title
    title_formatted = (
        row["title"].strip() if pd.notna(row["title"]) else "<Missing Title>"
    )

    # TODO: check for language
    # TODO: use LLM prompt to fix

    # Format expiration date safely
    if pd.notna(row["expire_at"]):
        try:
            expire_date_formatted = pd.to_datetime(
                row["expire_at"], errors="coerce"
            ).strftime("%d %b %Y")
        except (ValueError, TypeError, AttributeError):
            expire_date_formatted = "<Date Misformatted: DD MMM YYYY>"
    else:
        expire_date_formatted = "<Date Missing: DD MMM YYYY>"

    # Format company
    if pd.notna(row["company_slug"]):
        company_formatted = row["company_slug"].strip().upper()
    elif pd.notna(row["company_name"]):
        company_formatted = row["company_name"].strip().title()
    else:
        company_formatted = "<Company Missing>"

    # Determine remote status, handling NaN correctly
    if pd.isna(row["is_homebased"]) or not row["is_homebased"]:
        remote_formatted = ""
    else:
        remote_formatted = " [Remote]"

    # Format locations
    if isinstance(row["locations_names"], list) and row["locations_names"]:
        locations_formatted = " & ".join(
            f"#{location}" for location in row["locations_names"] if pd.notna(location)
        )
    else:
        locations_formatted = "<Location Missing>"

    # Format levels
    if isinstance(row["levels_clean"], list) and row["levels_clean"]:
        levels_formatted = "/".join(
            str(level) for level in row["levels_clean"] if pd.notna(level)
        )
    else:
        levels_formatted = "<Level Missing>"

    # Format areas
    if isinstance(row["areas_clean"], list) and row["areas_clean"]:
        areas_formatted = "/".join(
            str(area) for area in row["areas_clean"] if pd.notna(area)
        )
    else:
        areas_formatted = "<Area Missing>"

    # Ensure URL exists
    url_details = (
        row["url_details"] if pd.notna(row["url_details"]) else "<URL Missing>"
    )

    # Generate formatted job posting string
    job_posting = f"{title_formatted}, {areas_formatted} | {company_formatted}, {locations_formatted}{remote_formatted}, {levels_formatted} | {expire_date_formatted} {url_details}"

    return job_posting


## Test
df.iloc[29]
create_job_posting(df.iloc[495])

# Apply function over all rows
df["formatted_job_posting"] = df.apply(create_job_posting, axis=1)


### Export ###


# FIXME
data_folder = Path("data")
df.to_csv(data_folder / "output" / "job_postings_df.csv", index=False)