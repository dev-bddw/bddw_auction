# BDDW AUCTION

Quick POC for Django Auction Site

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# To Get Started

Create a new .stripe env file in .envs/.local/ and define your stripe test keys.

# Start docker using local config

docker-compose -f local.yml up --build

# create super user

docker-compose -f local.yml run --rm django python manage.py createsuperuser

# view the site

http://localhost:8000/
