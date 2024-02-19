#!/usr/bin/env bash

set -o errexit  # exit on error

pip install -r requirements.txt

python locallibrary/manage.py collectstatic --no-input
python locallibrary/manage.py migrate
