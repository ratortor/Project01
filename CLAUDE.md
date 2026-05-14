# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

From the repo root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Commands

All `manage.py` commands run from the `djangotutorial/` directory with the venv activated.

```bash
cd djangotutorial

# Run dev server (http://127.0.0.1:8000/)
python manage.py runserver

# Apply / create migrations
python manage.py migrate
python manage.py makemigrations [app_label]

# Run tests (whole project, one app, or one test)
python manage.py test
python manage.py test APP1
python manage.py test APP1.tests.SomeTestCase.test_method

# Django shell / create admin user
python manage.py shell
python manage.py createsuperuser
```

## Architecture

Standard Django layout from `django-admin startproject`:

- `djangotutorial/mysite/` — *project* package (configuración global): `settings.py`, root `urls.py`, `wsgi.py`, `asgi.py`. `DJANGO_SETTINGS_MODULE` is `mysite.settings`. The project itself is **not** an app and is not in `INSTALLED_APPS`.
- `djangotutorial/APP1/` — the only *app*. Registered in `INSTALLED_APPS` as `'APP1.apps.App1Config'`. Its `views.index` is wired to `''` from `mysite/urls.py`.
- `djangotutorial/db.sqlite3` — local SQLite database (gitignored; create it with `python manage.py migrate`).

When adding a new app, run `python manage.py startapp <name>` from `djangotutorial/`, then add `'<name>.apps.<Name>Config'` to `INSTALLED_APPS` and `include('<name>.urls')` from `mysite/urls.py`.

### Settings note

`mysite/settings.py` ships with `DEBUG = True`, an empty `ALLOWED_HOSTS`, and a hardcoded `SECRET_KEY` — development defaults from `django-admin startproject`. Treat any production-shaped change as out of scope unless the user asks.
