#!/bin/bash

cd /home/appuser/app/devhelp/

python manage.py migrate

exec "$@"