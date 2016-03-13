#!/usr/bin/env python
# encoding: utf-8

import threading
import time
import urlparse
import re
import urllib, urllib2, os, json, cookielib, random
import ConfigParser
import traceback
"""
@version: 1.0
@author: hiphp
@license: Apache Licence 
@contact: hi_php@163.com
@site: wuwenfu.cn
@software: PyCharm Community Edition
@file: dz_reply.py
@time: 2016/3/13 16:17
"""
#论坛编码
site_charset =False
#全局的。
formhash = False

#初始化。设置一些参数。避免重复获取。
def init_site():
    global site_url
    global  site_charset
    config = ConfigParser.RawConfigParser()
    config.read('keeptop.ini')
    site_url = config.get("global", "url")
    site_url = site_url.strip() #去空格


    #获取编码.不是utf-8就是gbk。todo:后期优化
    html =  urllib.urlopen(site_url).read()
    patter = re.compile('charset=utf-8',re.S)
    result = re.findall(patter,html)
    if result and len(result) > 0:
        site_charset = "utf-8"
    else:
        site_charset = "gbk"



#回复类。传递所有的参数进来。
class dz_reply():
    def __init__(self,host,username,pwd,tid,speed,msgs=[]):
        self.host = host
        self.username = username
        self.pwd = pwd
        self.tid = tid
        self.speed = speed
        self.msgs = msgs

        self.opener = self.login()

        pass
    def login(self):
        data = {
            "quickforward": "yes",
            "handlekey": "ls",
            "username": self.username,
            "password": self.pwd
        }  # urllib进行编码。
        post_data = urllib.urlencode(data)
        # 初始化一个CookieJar来处理Cookie。
        ckjar = cookielib.CookieJar()
        ckproc = urllib2.HTTPCookieProcessor(ckjar)
        # 实例化一个全局opener。
        opener = urllib2.build_opener(ckproc)
        # 获取cookie。
        login_url  = "%s/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1" % self.host
        req = urllib2.Request(login_url, post_data)
        result = opener.open(req)
        print result.read()
        return opener


if __name__ == '__main__':
    pass