#!/bin/bash

tools/with_venv.sh gunicorn -e 'ENV=dev' -c etc/dev/app.py gafly.wsgi
