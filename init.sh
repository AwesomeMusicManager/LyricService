#!/bin/bash
cd  src && gunicorn --max-requests 200 -w 4 --bind 0.0.0.0:${PORT} app:app