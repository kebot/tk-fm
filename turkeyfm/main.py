# !/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, Flask, request, session
from flask.views import View

app = Flask(__name__)

import time

@app.route('/')
def index():
    return render_template('index.html')


class TemplateView(View):
    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        return render_template(self.template_name)

class RestfulView(View):
    methods = ['GET', 'POST', 'DELETE', 'PUT']
    def dispatch_request(self):
        if request.method == 'GET':
            pass
        elif request.method == 'POST':
            pass
        elif request.method == 'DELETE':
            pass
        elif request.method == 'PUT':
            pass
app.add_url_rule('/api/', RestfulView.as_view('api'))


if __name__ == '__main__':
    app.debug = True
    app.run()
