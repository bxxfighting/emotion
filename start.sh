#!/bin/bash
gunicorn -c gunicorn.py -k gevent emotion.wsgi:application
