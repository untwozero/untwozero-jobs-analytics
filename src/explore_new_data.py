import json
import re
from pathlib import Path

import pandas as pd
from deep_translator import GoogleTranslator
from langdetect import detect


data_folder = Path("data")

with open(data_folder / "input" / "1.json") as f:
    json_data = json.load(f)


df = pd.DataFrame(json_data.get("jobs"))

####

## Wrangle time information
# Adjust time stamps

df["first_import_at"] = pd.to_datetime(df["first_import_at"], unit="s")
df["last_seen_at"] = pd.to_datetime(df["last_seen_at"], unit="s")
df["expire_at"] = pd.to_datetime(df["expire_at"], unit="s")

# Ensure columns are in datetime format, then strip time
date_columns = ["first_import_at", "last_seen_at", "expire_at"]

for col in date_columns:
    df[col] = pd.to_datetime(df[col]).dt.date


# Generalized extractor with optional post-processing
# FIXME: unique function names
def extract_field(data, prefix: str, postprocess=None):
    if isinstance(data, list):
        for item in data:
            if item.startswith(prefix + "__"):
                value = item.split(prefix + "__")[1]
                if postprocess:
                    return postprocess(value)
                return value
    return None


# Apply all field extractions
df["contract_name"] = df["contract_data"].apply(
    lambda x: extract_field(x, "contract_name")
)
df["experience_in_years"] = df["contract_data"].apply(
    lambda x: extract_field(
        x, "contract_experience", lambda v: int(v.replace("_years", ""))
    )
)
df["contract_family_name"] = df["contract_data"].apply(
    lambda x: extract_field(x, "contract_family_name")
)


df["level"] = df["contract_data"].apply(lambda x: extract_field(x, "contract_level"))
df["remote"] = df["contract_data"].apply(
    lambda x: extract_field(x, "tor_contract_remote_status")
)

# Remove leading underscore from contract_family_name
df["contract_family_name"] = df["contract_family_name"].str.lstrip("_")


# Enhanced extractor: works with custom separator
def extract_contract_data(data, prefix, postprocess=None, separator="__"):
    if isinstance(data, list):
        for item in data:
            if item.startswith(prefix + separator):
                value = item.split(prefix + separator)[1]
                if postprocess:
                    return postprocess(value)
                return value
    return None


df["international"] = df["contract_data"].apply(
    lambda x: extract_contract_data(x, "contract_family_staff", separator="_")
)


## preclean locations


# Function to clean each location in the list
def clean_locations(loc_list):
    if isinstance(loc_list, list):
        return [re.sub(r"^tor__", "", loc) for loc in loc_list]
    return loc_list  # in case it's not a list


# Apply the cleaning function
df["locations"] = df["locations"].apply(clean_locations)

##Raw Tags #needs adjustment

skills_map = {
    "data": ["data_analysis", "research_skills"],
    "management": ["program_management", "budget_management", "project_management"],
    "policy": [
        "policy_coordination",
        "environmental_policy",
        "sustainable_development",
    ],
    "facilitation": ["stakeholder_engagement", "workshop_facilitation"],
}


def clean_tags(tag_list):
    if isinstance(tag_list, list):
        return [re.sub(r"^\w+__", "", tag) for tag in tag_list]
    return []


df["cleaned_tags"] = df["raw_tags"].apply(clean_tags)


def tag_matcher(cleaned_list, keywords):
    return any(tag in keywords for tag in cleaned_list)


for skill, keywords in skills_map.items():
    df[f"requires_{skill}_skills"] = df["cleaned_tags"].apply(
        lambda tags: tag_matcher(tags, keywords)
    )

##Change job titel language where needed


# Function to detect language and translate if needed
def translate_if_not_english(text):
    try:
        if detect(text) != "en":
            return GoogleTranslator(source="auto", target="en").translate(text)
        return text
    except Exception:
        return text  # fallback if detection fails


# Apply to your 'title' column
df["title"] = df["title"].apply(translate_if_not_english)

##Attempt Quintet callsification


# Define your job categorization dictionary
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


# Function to classify based on raw_tags, title, and slug
def classify_quintet(row):
    text = ""

    # Combine text from all 3 columns (flatten list if raw_tags is list)
    if isinstance(row["raw_tags"], list):
        text += " ".join(row["raw_tags"])
    elif pd.notna(row["raw_tags"]):
        text += str(row["raw_tags"])

    text += " " + str(row["title"]) + " " + str(row["slug"])

    # Loop through all categories and patterns
    for category, patterns in job_categorization_dict.items():
        for pattern in patterns:
            if re.search(pattern, text, flags=re.IGNORECASE):
                return category
    return "NA"


# Apply to DataFrame
df["quintet"] = df.apply(classify_quintet, axis=1)

###############


# df.to_pickle(data_folder / "output" / "explored_data.pkl")
