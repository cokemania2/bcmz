#!/bin/bash

python3 -m venv venv
. venv/bin/activate
python3 manage.py migrate
python3 manage.py runserver