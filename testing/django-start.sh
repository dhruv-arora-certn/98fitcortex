#!/bin/bash

exec gunicorn testing.wsgi --reload --workers=3 --bind 0:8000
