# DS4300 Final Project: NEUFriends

## Setup & Installation

This web app uses Python 3.10, pipenv, and Django. If you haven't already, please install
Python 3.10 and pipenv (a simple Google search should get you what you need).

After installing those, you should be able to clone this repo, cd into it, and install all the
dependencies (including Django) with `pipenv install`.

After that, you should be able to run a development server with `python3 manage.py runserver`.

## Running Django commands

If you're following Django tutorials, you might notice that you can't run Django 
specific commands like `django-admin ...` - this is because we're using pipenv. To setup
your shell to recognize that Django has been installed, you must run `pipenv shell` first.

## Miscellaneous

This repo will never be used in production, so things like exposed secret keys aren't an issue. 