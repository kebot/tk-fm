#
#
# Makefile for Turkey
#
#

all: coffee

coffee:
	coffee -c turkeyfm/public/coffee/*.coffee

install:
	npm install -g juggernaut
	virtualenv venv
	venv/bin/pip install -r requirement.txt

run:
	redis-server redis.conf
	nohup juggernaut &
	nohup coffee -c -w turkeyfm/public/coffee/*.coffee &
	venv/bin/python app.py

watch:
	coffee -c -w turkeyfm/public/coffee/*.coffee

