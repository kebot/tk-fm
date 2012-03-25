#!/usr/bin/env bash
hash uwsgi 2>&- || { echo >&2 "I require uwsgi but it's not installed. Aborting."; exit 1;}

killall uwsgi
sleep 2
nohup uwsgi -s /tmp/uwsgi.sock --file `pwd`/turkeyfm/app.py
