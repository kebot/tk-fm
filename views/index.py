#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, session
from turkeyfm import app

@app.route('/', methods=['GET'])
def index():
    """docstring for index"""
    return render_template('index.html')


