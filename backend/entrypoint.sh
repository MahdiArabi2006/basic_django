#!/bin/sh
set -e

if [ "$1" = "gunicorn" ]; then
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
fi

exec "$@"
