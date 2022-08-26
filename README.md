# This project is a test automation for WEHAGO web application.

To run the project a user has to install [Poetry](https://python-poetry.org/).

---

## Before RUN

1. **JAVA** installed.
2. **npm** and **nodejs** installed.
3. Install **[Allure Framwork](https://github.com/allure-framework/allure2)**. It can be installed
   using **[scoop](https://scoop.sh/)** package manager.

## Run

1. `poetry shell` - activate virtual environment.
2. `poetry install` - install dependencies.
3. `poetry run pytest --alluredir="../allure-report" /tests/test-web-automation.py` - run the tests. Or run from IDE run
   configuration with additional arguments: `--alluredir="../allure-report"`.
4. `deactivate` - to deactivate virtual environment.

## Allure report server

Run `allure serve {path to project}/allure-report` to activate allure report server.