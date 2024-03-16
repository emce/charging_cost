#!/bin/sh
set -e
python manage.py migrate --no-input
python manage.py collectstatic --no-input
gunicorn -b 0.0.0.0:9080 charging_cost.wsgi --timeout 200 --workers=5 --capture-output --access-logfile /logs/gunicorn-access.log --error-logfile /logs/gunicorn-error.log
