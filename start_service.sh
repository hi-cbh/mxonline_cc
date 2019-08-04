#!/bin/bash

python3 /home/docker/code/mxonline/manage.py migrate 
python3 /home/docker/code/mxonline/manage.py collectstatic --noinput
supervisord -n

