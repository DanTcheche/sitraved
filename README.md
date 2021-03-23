# Sitraved
Recommendation system

## Setup

Build project:
- Install [docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/).

Try next commands with `sudo` if you get permission errors.
- `docker-compose build`.
- `docker-compose up -d`.
- Server will run in port 8080.

### Requirements

This projects requires python 3.6.
Python 3 can be installed with [pyenv](https://github.com/pyenv/pyenv).

1. Use [pyenv-installer](https://github.com/pyenv/pyenv-installer) for installing pyenv
1. See which python versions are available: `pyenv install --list`
1. Install python 3. Example: `pyenv install 3.7.5` (3.7.0 or higher)
1. `pyenv shell 3.7.5`
1. `poetry shell`


## Install new dependencies
This project uses [poetry](https://python-poetry.org/). as a dependency manager.
- `poetry shell`.
- `poetry add {dependency_name}`.


## Create new apps
1) Create a folder in `my_project/apps/` with the app name.
1) Run `python manage.py startapp {app_name} my_project/apps/{folder_name}`.
1) Add the app to you LOCAL_APPS in the `base.py`.
1) Add the apps urls in `settings/urls.py`.



