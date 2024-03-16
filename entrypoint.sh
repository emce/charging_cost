#!/bin/sh
set -e
touch .env
echo "DEBUG=0" >> .env
python manage.py migrate --no-input
python manage.py collectstatic --no-input
gunicorn -b 0.0.0.0:9080 charging_cost.wsgi --timeout 200 --workers=5
