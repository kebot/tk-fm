#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template
from turkeyfm import app

@app.route('/', methods=['GET'])
def index():
    """docstring for index"""
    return render_template('index.html')

