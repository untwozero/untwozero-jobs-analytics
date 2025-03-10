# UN 2.0 – Jobs Analytics

## Prerequisites
Ensure you have the following installed:
- [ ] [Visual Studio Code](https://code.visualstudio.com/)
- [ ] [Python](https://www.python.org/downloads/) (Latest version 3.13)
- [ ] [Git](https://git-scm.com/)

## Installation

### Clone the Repository

```sh
git clone https://github.com/untwozero/untwozero-jobs-analytics.git
cd untwozero-jobs-analytics
```
### Setting Up a Virtual Environment

In the project folder, create a virtual environment (venv) and activate it.

**On macOS/Linux:**
```sh
python3 -m venv .venv
source .venv/bin/activate
```

**On Windows:**
```sh
python -m venv .venv
.venv\Scripts\activate
```

### Installing Dependencies
**Once the virtual environment is activated**, install the required packages via `pip` ("Pip Installs Packages"):

```sh
pip install --upgrade pip
pip install -r requirements.txt
```

### Setting Environment Variables

- Rename `.env-example` to `.env`
- Now, copy in the secret API Key


## Access Data

- https://raw.githubusercontent.com/untwozero/untwozero-jobs-analytics/refs/heads/main/data/public/clean_jobs_df.csv


## Acknowledgments

We would like to extend our sincere gratitude to [UNTalent](https://untalent.org/jobs) for providing us with access to their [API](https://github.com/UNTalent/Documentation?tab=readme-ov-file), which has made this project possible. A special thank you to [Nathanaël Khodl](https://github.com/Khodl) for their support and dedication in making this resource available.