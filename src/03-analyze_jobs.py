import csv
import re
from pathlib import Path

import pandas as pd

DATA_DIR = Path("data")
# df = pd.read_csv(DATA_DIR / "public" / "clean_jobs_df.csv")
df = pd.read_pickle(DATA_DIR / "public" / "clean_jobs_df.pkl")


# -------------------------------
# 1. UN 2.0 Keyword Dictionary (with Regex)
# -------------------------------
job_categorization_dict = {
    "Digital": [
        r"\b(app(?:lication)? developer|app(?:lication)? development)\b",
        r"\b(back[- ]?end developer|back[- ]?end development|backend developer|backend development)\b",
        r"\b(chief information officer|cto|connectivity|cyber(?: security|security| developer| development)?)\b",
        r"\b(digitali[sz]ation|digitization|ict|information (?:management|systems|technology))\b",
        r"\b(internet of things|it (?:developer|development|expert|associate|advisor|consultant|officer))\b",
        r"\b(process automation|software (?:architect|developer|development|engineer|engineering))\b",
        r"\b(system(?:s)? (?:engineer|engineering)|telecomm(?:unications?)?)\b",
        r"\b(ui/ux|ux/ui|ui(?: &|/)ux|ux(?: &|/)ui|ui(?: design| designer| developer)|ux(?: design| designer| developer))\b",
        r"\b(web (?:developer|development|design|programming)|wordpress (?:developer|development))\b",
    ],
    "Data": [
        r"\b(ai|artificial intelligence|analytics|automation (?:engineer|specialist))\b",
        r"\b(business (?:analyst|intelligence)|data|geographic information|geospatial)\b",
        r"\b(gis (?:analyst|specialist)|machine learning|ml (?:consultant|expert|engineer|developer|development))\b",
        r"\b(monitoring|performance (?:analytics|metrics)|statistic(?:ian)?|statistical|statistics)\b",
    ],
    "Innovation": [
        r"\b(concept (?:developer|development)|creative technologist|design thinking)\b",
        r"\b(emerging technolog(?:y|ies)|frontier technolog(?:y|ies)|innovation|innovator)\b",
        r"\b(open science|portfolio management|program management consultant|r&d|recovery roadmap|research and development)\b",
        r"\b(solutions mapping)\b",
    ],
    "Strategic Foresight": [
        r"\b(anticipation|strategy (?:consultant|development)|early ?warning|foresight|forecast(?:ing|er)?)\b",
        r"\b(futurist|plan(?:ner|ning)?|preparedness|resource mobilization|risk|scenario(?:s)?)\b",
        r"\b(strateg(?:ic|ist|y)|trend(?:s)?|vision(?:ary)?)\b",
    ],
    "Behavioral Science": [
        r"\b(behavior(?:al)?|behaviour(?:al)?)\b",
        r"\b(change management|cognition|cognitive|communications strategy|community|communal)\b",
        r"\b(human factors|organisational behaviour|organizational behaviour|psychologist|social (?:network|cognition|policy|psychologist|theory))\b",
    ],
}

# -------------------------------
# 2. UN-related Orgs (Example)
# -------------------------------
IMPORTANT_ORG_SUBSTRINGS = [
    "Food and Agriculture Organization",
    "International Atomic Energy Agency",
    "International Labour Organization",
    "International Organization for Migration",
    "United Nations Secretariat",
    "Joint United Nations Programme on HIV/AIDS",
    "United Nations Development Programme",
    "United Nations Educational, Scientific and Cultural Organization",
    "United Nations Population Fund",
    "High Commissioner for Refugees",
    "International Computing Centre",
    "Children's Fund",
    "United Nations Office for Project Services",
    "United Nations Volunteers",
    "World Food Programme",
    "World Health Organization",
    "World Intellectual Property Organization",
    "World Trade Organization",
]


# -------------------------------
# 3. Match Title to UN 2.0 Categories (Using Regex)
# -------------------------------
def match_un2_0_categories(title: str, dictionary: dict) -> list:
    """
    Matches job title against UN 2.0 keywords using regex.

    Args:
        title (str): The job title to categorize.
        dictionary (dict): A mapping of categories to regex patterns.

    Returns:
        list: A list of matched categories.
    """
    if not isinstance(title, str) or not title.strip():
        return []

    lowered_title = title.lower()
    categories_found = [
        category
        for category, patterns in dictionary.items()
        if any(re.search(pattern, lowered_title, re.IGNORECASE) for pattern in patterns)
    ]

    return categories_found


# -------------------------------
# 6. Exclude Intern/Internship & Filter Out "National" and "Local"
# -------------------------------

# FIXME: add these as variables to the data frame

# df["levels_clean"].explode().value_counts()

df["is_internship_level"] = df["levels_clean"].apply(
    lambda x: any("internship" in level.lower() for level in x)
)

df["is_internship_title"] = df["title"].str.contains(
    r"\bintern(?:ship)?\b", flags=re.IGNORECASE, na=False, regex=True
)

df["is_internship"] = df["is_internship_level"] | df["is_internship_title"]


# df.groupby(["is_internship_level", "is_internship_title"]).size().reset_index(name="count")
# intern_df = df[(df["is_internship_level"]) | (df["is_internship_title"])][
#     ["title", "levels_clean", "is_internship_level", "is_internship_title"]
# ]


# TODO: improve
df["is_national_or_local"] = df["title"].str.contains(
    r"\b(?:national|local)\b", flags=re.IGNORECASE, na=False, regex=True
)


# df["is_national_or_local"].value_counts()

# filtered_jobs = df[~(df["is_internship"]) & ~(df["is_national_or_local"])]

# print(
#     f"After filtering out internships, 'national', and 'local', {len(filtered_jobs)} out of {len(df)} jobs remain."
# )

# -------------------------------
# 7. Filter by UN 2.0 categories
# -------------------------------

df["job_quintet"] = df["title"].map(
    lambda title: match_un2_0_categories(title, job_categorization_dict)
)

df["is_un2.0_relevant"] = df["job_quintet"].apply(
    lambda x: bool(x)
)  # Ensures correct evaluation for empty lists


relevant_jobs = df[df["is_un2.0_relevant"]]
print(f"Found {len(relevant_jobs)} relevant jobs based on UN 2.0 keywords.")


# -------------------------------
# 8. Filter by UN-related Orgs
# -------------------------------
df["is_un_org"] = df["company_name"].apply(
    lambda company: any(
        sub.lower() in company.lower() for sub in IMPORTANT_ORG_SUBSTRINGS
    )
)

# df[["company_name", "is_un_org"]]

data_folder = Path("data")
df.to_csv(data_folder / "output" / "analyzed_jobs_df.csv", index=False)


# TODO: preprocess list columns for Power BI, deal with multiple locations, etc.

df_final = df[
    [
        "url",  # TODO: could be hashed as unique ID
        "slug",  # TODO: could be hashed as unique ID
        "title",  # TODO: could be further cleaned
        "description",  # TODO: still needs to be cleaned/processed
        # "areas", # processed
        # "levels", # processed
        # "company", # processed
        # "locations", # processed
        "expire_at",  # TODO: fill missings
        "is_homebased",  # TODO: fill missings
        "areas_clean",
        "levels_clean",
        "locations_names",
        "locations_latitudes",
        "locations_longitudes",
        "company_name",
        "company_slug",
        "url_apply",  # TODO: fix redirects
        "url_details",  # TODO: fix redirects
        # "is_internship_level", # intermediary
        # "is_internship_title", # intermediary
        "is_internship",  # combined
        "is_national_or_local",
        "job_quintet",  # TODO: process in a way that is nicely ingestable for Power BI and deal with multiple matches
        "is_un2.0_relevant",
        "is_un_org",
    ]
]


df_final.to_csv(data_folder / "public" / "analyzed_jobs_df.csv", index=False)

###### FIXME


# print(f"After filtering by UN org, found {len(final_jobs)} jobs.")

# if not final_jobs:
#     print("No final jobs matched the UN org filter. Exiting.")

# # -------------------------------
# # 9. Export to CSV
# # -------------------------------
# csv_filename = "un2_0_jobs_filtered.csv"
# fieldnames = ["title", "categories", "url", "company", "description", "locations"]

# with open(csv_filename, mode="w", newline="", encoding="utf-8") as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#     for job in final_jobs:
#         writer.writerow(
#             {
#                 "title": job.get("title", ""),
#                 "categories": ", ".join(job.get("categories", [])),
#                 "url": job.get("url", ""),
#                 "company": job.get("company", {}).get("name", ""),
#                 "description": job.get("description", "")[:200] + "...",
#                 "locations": "; ".join(
#                     loc.get("name", "") for loc in job.get("locations", [])
#                 ),
#             }
#         )

# print(f"\nCSV export complete! See '{csv_filename}'.")
# print("Done.")
