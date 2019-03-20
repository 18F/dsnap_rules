#!/usr/bin/env bash
[ $CF_INSTANCE_INDEX -eq 0 ] && python manage.py migrate
python manage.py collectstatic --noinput
gunicorn -k gevent -w 4 -b 0.0.0.0:$PORT rules_service.wsgi
