#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from hashlib import md5

MUSIC_CDN_LOAD_BALANCE = {
    '0': 'netcenter',
    '9': 'netcenter',
    '8': 'netcenter',
    '7': 'netcenter',
    '6': 'netcenter',
    'default': 'chinacache',
}

def timestamp_sign(path, secret, domain):
    """prepend timestamp-based signature for CDN."""
    assert path.startswith('/')
    timestamp = time.strftime('%Y%m%d%H%M')
    signature = md5(secret+timestamp+path).hexdigest()
    return 'http://%s/%s/%s%s' % (domain, timestamp, signature, path)

def sign_for_chinacache(path, channel='mr'):
    assert channel in ('mr', 'vt')
    return timestamp_sign(path, 'db44ed4c9acc',
                          '%s4.douban.com' % channel)


def within_warmup_time_range():
    # replicate files on all cdn nodes between 2am~8am
    return 2 <= (time.time() / 3600 + 8) % 24 < 8

def music_url(path, use_cdn=None, time_based_warmup=True):
    if use_cdn is None:
        use_cdn = not DEVELOP_MODE

    path = str(path)

    if not use_cdn:
        return VIEW_PHOTO_SERVER + path

    if time_based_warmup and within_warmup_time_range():
        cdn_funcs = [sign_for_chinacache]*6 + [sign_for_netcenter]*4
        func = random.choice(cdn_funcs)
    else:
        id_last = path[-5]  # path should end with '.mp3'
        cdn = MUSIC_CDN_LOAD_BALANCE.get(id_last, MUSIC_CDN_LOAD_BALANCE['default'])
        if cdn == 'netcenter':
            func = sign_for_netcenter
        elif cdn == 'chinacache':
            func = sign_for_chinacache
        elif cdn == 'dnion':
            func = sign_for_dnion
        else:
            raise Exception("unkown cdn: %r" % cdn)

    return func(path, channel='mr')


if __name__ == '__main__':
    print music_url('/view/song/small/p1027451.mp3', True, True)
