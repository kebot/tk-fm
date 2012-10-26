#!/usr/bin/env python
# -*- coding: utf-8 -*-
from turkeyfm import app
import urllib2
import os
from flask import redirect, Response

TMP_PATH = '/tmp/turkeyfm/'

AUDIO_PATH = os.path.join(app.static_folder, 'audio')

@app.route('/audio/<int:sid>/<path:url>')
def pass_audio(sid, url):
    sid = str(sid)
    tmp_name = TMP_PATH+sid+'.mp3.tmp'
    filename = os.path.join(AUDIO_PATH, sid+'.mp3')

    if os.path.exists(filename):
        redirect('/public/audio/%s.mp3' % sid)
    else:
        LENGTH = 1024
        url = 'http://' + url
        def generate():
            #fp = open(tmp_name, 'w+')
            up = urllib2.urlopen(url)
            for value in up:
                #fp.write(value)
                yield value
            #fp.close()
            #os.rename(tmp_name, filename)
        return Response(generate(), mimetype='audio/mpeg')


