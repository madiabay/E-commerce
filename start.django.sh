#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python /app/code/manage.py makemigrations
python /app/code/manage.py migrate
python /app/code/manage.py collectstatic --noinput

cd /app/code
daphne -b 0.0.0.0 -p 8000 src.asgi:application
