#!/bin/bash

gunicorn --bind 0.0.0.0:80 --workers 6 --keep-alive 1 --timeout 30 --worker-class gevent security_cam.wsgi:app
