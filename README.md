# UN 2.0 – Jobs Analytics

## Prerequisites
Ensure you have the following installed:
- [ ] [Visual Studio Code](https://code.visualstudio.com/)
- [ ] [Python](https://www.python.org/downloads/) (Latest version 3.13)
- [ ] [Git](https://git-scm.com/)

## Installation

### Clone the Repository

First, you will have to clone the remote repository locally. 

You can either first open **Visual Studio Code** and then click on `Clone Git Repository...` and select 
`untwozero/untwozero-jobs-analytics`.

Or in a **Terminal**, navigate to the folder where you want to clone the repo into and then run:

```sh
git clone https://github.com/untwozero/untwozero-jobs-analytics.git
```

To enter the folder and open it in Visual Studio Code, run:

```sh
cd untwozero-jobs-analytics
code .
```

If the `code` command does not work, follow the steps outlined [here](https://code.visualstudio.com/docs/setup/mac#_configure-the-path-with-vs-code).



### Setting Up a Virtual Environment

Inside the **opened project folder**, create a virtual environment (venv) and activate it.

#### On MacOS/Linux

To create the virtual environment, use the `venv` command (you only have to do this once).

```sh
python3 -m venv .venv
```

To activate it, run the activate script. You will have to do this everytime you want to make changes to the virtual environment. For example, before installing new dependencies.

```sh
source .venv/bin/activate
```

#### On Windows

Almost the same:

```sh
python -m venv .venv
```

```sh
.venv\Scripts\activate
```

### Installing Dependencies
**Once the virtual environment is activated**, install the required packages via `pip` ("Pip Installs Packages"):

First, make sure pip itself is up-to-date.

```sh
pip install --upgrade pip
```

Then, install all packages from the `requirements.txt` file.
 
```sh
pip install -r requirements.txt
```

To install other packages, you can use: `pip install <package>`


### Setting Environment Variables

- Copy and rename the `.env-example` file to `.env`
- Now, paste in the secret API Key


## Web Access Data

- https://raw.githubusercontent.com/untwozero/untwozero-jobs-analytics/refs/heads/main/data/public/clean_jobs_df.csv


## Acknowledgments

We would like to extend our sincere gratitude to [UNTalent](https://untalent.org/jobs) for providing us with access to their [API](https://github.com/UNTalent/Documentation?tab=readme-ov-file), which has made this project possible. 
A special thank you to [Nathanaël Khodl](https://github.com/Khodl) for their support and dedication in making this resource available.