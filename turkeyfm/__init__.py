#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.mako import MakoTemplates

app = Flask(__name__, static_folder='public')

app.config.update({
    'MAKO_INPUT_ENCODING': 'utf-8',
    'MAKO_OUTPUT_ENCODING': 'utf-8'
})

mako = MakoTemplates(app)
app.template_folder = 'templates'

import turkeyfm.controller

