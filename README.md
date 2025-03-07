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

## Access Data

- https://raw.githubusercontent.com/untwozero/untwozero-jobs-analytics/refs/heads/main/data/public/clean_jobs_df.csv

