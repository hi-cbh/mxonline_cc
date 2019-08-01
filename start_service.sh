#!/bin/bash

python3 /home/docker/code/mxonline/manage.py migrate && supervisord -n

