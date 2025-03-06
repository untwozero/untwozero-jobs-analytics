# cleaning bash script

source .venv/bin/activate
black src/
isort src/
pip freeze > requirements.txt