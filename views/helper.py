#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import abort, g, session, jsonify
from douban_hack import WebClient, DoubanFMClient as APIClient

from functools import wraps


def require_api_login(func):
    @wraps(func)
    def _(*args, **kwargs):
        is_login = False
        info = session.get('api_info')
        if info:
            g.api_client = APIClient(login_info=info)
            is_login = True
        if is_login:
            return func(*args, **kwargs)
        else:
            return abort(403)
    return _


def require_web_login(func):
    @wraps(func)
    def _(*args, **kwargs):
        #is_login = False
        cookie_info = session.get('cookie_info')
        if cookie_info:
            g.web_client = WebClient(cookies=cookie_info)
        else:
            g.web_client = WebClient()
            #is_login = True
        #if is_login:
        return func(*args, **kwargs)
        #else:
            #return abort(403)
            #return jsonify({'r': 1, 'err': 'unauthorized'})
    return _


if __name__ == '__main__':
    @require_api_login
    def user_info():
        return 'successed'

    print user_info()


