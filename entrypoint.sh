#!/bin/sh
set -e

echo "Applying migrations..."
python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "Creating users..."
python app/create_users.py || true

echo "Simulating 100 conversations..." 
python app/simulate.py || true

echo "Starting Gunicorn..."
exec gunicorn project.wsgi:application \
     --bind 0.0.0.0:8000 \
     --workers 3 \
     --access-logfile - \
     --error-logfile -
