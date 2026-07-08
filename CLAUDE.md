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

All `manage.py` commands run from the repo root with the venv activated.

```bash
# Run dev server (http://127.0.0.1:8000/)
python manage.py runserver

# Apply / create migrations
python manage.py migrate
python manage.py makemigrations [app_label]

# Run tests (whole project, one app, or one test)
python manage.py test
python manage.py test classes
python manage.py test classes.tests.SomeTestCase.test_method

# Django shell / create admin user
python manage.py shell
python manage.py createsuperuser
```

## Architecture

Flattened Django layout (the `manage.py`, project package, and apps all live at the repo root):

- `mysite/` — *project* package (configuración global): `settings.py`, root `urls.py`, `wsgi.py`, `asgi.py`. `DJANGO_SETTINGS_MODULE` is `mysite.settings`. The project itself is **not** an app and is not in `INSTALLED_APPS`.
- `classes/` — the only *app* (domain: class management). Registered in `INSTALLED_APPS` as `'classes.apps.ClassesConfig'`. Its `views.index` is wired to `''` from `mysite/urls.py`.
- `db.sqlite3` — local SQLite database at the repo root (gitignored; create it with `python manage.py migrate`). Path resolves from `BASE_DIR = Path(__file__).resolve().parent.parent` in `mysite/settings.py`.

When adding a new app, run `python manage.py startapp <name>` from the repo root, then add `'<name>.apps.<Name>Config'` to `INSTALLED_APPS` and `include('<name>.urls')` from `mysite/urls.py`.

### Settings note

`mysite/settings.py` ships with `DEBUG = True`, an empty `ALLOWED_HOSTS`, and a hardcoded `SECRET_KEY` — development defaults from `django-admin startproject`. Treat any production-shaped change as out of scope unless the user asks.
