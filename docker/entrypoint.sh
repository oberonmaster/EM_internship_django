#!/bin/bash

# Ждём БД, если надо:
# echo "Waiting for database..."
# until nc -z db 5432; do
#   sleep 1
# done

echo "Applying migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting app..."
exec "$@"
