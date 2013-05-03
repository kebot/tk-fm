#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @TODO redis session be created
# key: <session.id> value: <deviceid>

import uuid
from redis import Redis
from yafa.session import RedisSessionInterface, RedisSession
from flask import request

import logging
logger = logging.getLogger('session')

class CustomSession(RedisSession):
    def __init__(self, initial=None,
            sid=None,
            new=False,
            device_id=None):
        super(CustomSession, self).__init__(initial, sid, new)
        self.device_id = None
        if device_id is not None:
            self.device_id = device_id


class SessionInterface(RedisSessionInterface):
    """ Redis Session Interface with extra feature """

    session_class = CustomSession

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        logger.info(request)
        if not sid:
            logger.info('session: no sid -- session_key:', app.session_cookie_name)
            logger.info(request.cookies)
            return self._create_session()
        val = self.redis.get(self.prefix + sid)
        if val is not None:
            data = self.serializer.loads(val)
            return self.session_class(data, sid=sid)
        logger.info('session: no value')
        return self._create_session(new=True)


    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            self.redis.delete(self.prefix + session.sid)
            if session.modified:
                response.delete_cookie(app.session_cookie_name,
                                       domain=domain)
            return
        redis_exp = self.get_redis_expiration_time(app, session)
        cookie_exp = self.get_expiration_time(app, session)
        _exp = int(redis_exp.total_seconds())

        if session.device_id is not None:
            session.__setitem__('device_id', session.device_id)
            device_key = self._device_id_key(session.device_id)
            self.redis.setex(device_key, session.sid, _exp)

        val = self.serializer.dumps(dict(session))
        self.redis.setex(self.prefix + session.sid, val, _exp)
        response.set_cookie(app.session_cookie_name, session.sid,
                            expires=cookie_exp, httponly=True,
                            domain=domain)


    def _generate_device_id(self):
        return str(uuid.uuid4())

    def _device_id_key(self, device_id):
        return self.prefix + 'device:' + device_id

    def _create_session(self, new=False):
        sid = self.generate_sid()
        # connect device_id <-> session_id
        device_id = self._generate_device_id()
        return self.session_class(sid=sid, device_id=device_id, new=new)

def init_redis_session(app):
    app.config.setdefault('REDIS_SERVER_CONFIG', dict(
        host='localhost',
        port=6379,
        db=0,
        password=None,
    ))
    app.config.setdefault('SESSION_PREFIX', u'session:')
    config = app.config.get('REDIS_SERVER_CONFIG')

    redis_client = Redis(**config)
    app.session_interface = SessionInterface(redis=redis_client,
            prefix=app.config.get('SESSION_PREFIX'))
    return app

