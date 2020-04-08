#!/bin/bash
echo "run migrations"
python manage.py migrate
echo "migrations ran"
exec "$@"
