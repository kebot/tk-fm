#!/usr/bin/env python
# encoding: utf-8

import re
import json
import pickle
import urllib
import urllib2
import os.path
import cookielib
from BeautifulSoup import BeautifulSoup


class Client(object):
    re_comment = re.compile(r"<!-.*?-->|<!.*?-->|<!--.*?>",re.M|re.S|re.I)
    re_bracket = re.compile(r"\(\d+\)")
    _cookie_store = 'cookie.txt'
    
    def __init__(self):
        self.cookiejar = cookielib.MozillaCookieJar()
        if os.path.exists(self._cookie_store):
            self.cookiejar.load(self._cookie_store)
        cookie_support= urllib2.HTTPCookieProcessor(self.cookiejar)
        self.opener = urllib2.build_opener(cookie_support)
        headers = [
            ("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.220 Safari/535.1"),
        ]
        self.opener.addheaders = headers
        self._is_dj = None
        
    def get_captcha(self, url=None):
        if url is None:
            url = "http://www.douban.com/accounts/login"
        content = self.opener.open(url).read()
        content = self.re_comment.sub("", content)
        soup = BeautifulSoup(content)
        try:
            captcha_img = soup.find("img", {"class":"captcha_image"})["src"]
            captcha_id = soup.find("input", {"name":"captcha-id"})["value"]
        except:
            return (None, None)
        return (captcha_img, captcha_id)
    
    @property
    def is_dj(self):
        if self._is_dj is None:
            self._is_dj = self.search('xx') is not False
        return self._is_dj

    def request(self, url, data=None):
        request = None
        if data is None:
            request = urllib2.Request(url)
        else:
            request = urllib2.Request(url, urllib.urlencode(data))
        response = self.opener.open(request)
        return response
    
    def login(self, username, password, captcha_sol=None, captcha_id=None):
        url = "https://www.douban.com/accounts/login"
        data = { "source" : "simple",
                 "redir" : "http://www.douban.com/",
                 "form_email" : username,
                 "form_password" : password,
                 "remember" : "on",
                 "user_login" : "登录",
               }
        if captcha_sol is not None:
            data["captcha-solution"] = captcha_sol
            data["captcha-id"] = captcha_id
        response = self.request(url, data)
        if self.is_dj:
            self.cookiejar.save(self._cookie_store)
        return response
    
    def search(self, keyword, limit=200):
        url = "http://douban.fm/j/open_channel/creation/search?"
        data = {'keyword': keyword.encode('utf8'), 'limit': limit}
        print url + urllib.urlencode(data)
        jsondata = json.loads(self.request(url + urllib.urlencode(data)).read())
        if jsondata.get('status') is False:
            return False
        else:
            return jsondata.get('data')


client = Client()
    
if __name__ == "__main__":
    username = 'test@gmail.com'
    password = 'test'
    robot = Client()
    (captcha_img, captcha_id) = robot.get_captcha()
    if captcha_img is not None:
        print captcha_img
        captcha_sol = raw_input()
        robot.login(username, password, captcha_sol, captcha_id)
    else:
        robot.login(username, password)
    print robot.search("xx")
