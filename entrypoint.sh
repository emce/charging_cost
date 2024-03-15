#!/bin/sh
set -e
python3 manage.py migrate --no-input
python3 manage.py collectstatic --no-input
gunicorn -b 0.0.0.0:9080 charging.wsgi --timeout 200 --workers=5