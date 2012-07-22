#!/usr/bin/env python
# -*- coding: utf-8 -*-

from turkeyfm import app

app.secret_key = 'somthing is really secret!'

if __name__ == '__main__':
    app.debug = True
    app.run()

