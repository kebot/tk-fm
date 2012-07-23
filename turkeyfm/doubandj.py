#!/usr/bin/env python
# encoding: utf-8

import re
import json
import urllib2
import cookielib
from BeautifulSoup import BeautifulSoup

class Robot(object):
    re_comment = re.compile(r"<!-.*?-->|<!.*?-->|<!--.*?>",re.M|re.S|re.I)
    re_bracket = re.compile(r"\(\d+\)")
    
    def __init__(self, username, password):
        if username and password:
            self._username = username
            self._password = password
        cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        self.opener = urllib2.build_opener(cookie_support)
        headers = [("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.220 Safari/535.1")]
        self.opener.addheaders = headers
        
    def get_captcha(self, url=None):
        if url is None:
            url = "http://www.douban.com/accounts/login"
        content = self.opener.open(url).read()
        content = self.re_comment.sub("", content)
        soup = BeautifulSoup(content)
        print content.decode("utf-8")
        try:
            captcha_img = soup.find("img", {"class":"captcha_image"})["src"]
            captcha_id = soup.find("input", {"name":"captcha-id"})["value"]
        except:
            return (None, None)
        return (captcha_img, captcha_id)
    
    def is_dj(self):
        if 
    
    def request(self, url, data=None):
        request = None
        if data is None:
            request = urllib2.Request(url)
        else:
            request = urllib2.Request(url, urllib.urlencode(data))
        response = self.opener.open(request)
        return response
    
    def login(self, captcha_sol=None, captcha_id=None):
        url = "https://www.douban.com/accounts/login"
        data = { "source" : "simple",
                 "redir" : "http://www.douban.com/",
                 "form_email" : self._username,
                 "form_password" : self._password,
                 "remember" : "on",
                 "user_login" : "登录",
               }
        if captcha_sol is not None:
            data["captcha-solution"] = captcha_sol
            data["captcha-id"] = captcha_id
        return self.request(url, data)
    
    def search(self, keyword, limit=20):
        url = "http://douban.fm/j/open_channel/creation/search?keyword=%s&limit=%d" % (keyword, limit)
        jsondata = json.loads(self.request(url).read())
        if jsondata.status is False:
            return False
        else:
            return jsondata.data

    
if __name__ == "__main__":
    username = 'test@yaofur.com'
    password = 'testdouban'
    robot = Robot(username, password)
    (captcha_img, captcha_id) = robot.get_captcha()
    if captcha_img is not None:
        print captcha_img
        captcha_sol = raw_input()
        robot.login(captcha_sol, captcha_id)
    else:
        robot.login()
    print robot.search("xx")
    