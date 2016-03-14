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




#回复类。传递所有的参数进来。
class dz_reply(threading.Thread):
    def __init__(self,threadName,event,host,username,pwd,tid,speed,msgs=[]):
        threading.Thread.__init__(self,name=threadName)
        self.threadEvent = event

        self.host = host
        self.username = username
        self.pwd = pwd
        self.tid = tid
        self.speed = speed
        self.msgs = msgs
        self.count = 0 #回帖的次数

        self.formhash = False
        self.fid = False
        self.status =False

        self.setEncode()

        self.opener = self.login()

        pass
    def run(self):
        print "%s is ready" % self.name
        self.threadEvent.wait()
        print "%s run!" % self.name

        self.getFormhash()
        self.getFid()
        while True:
            if self.threadEvent.isSet():
                self.reply()
                time.sleep(float(self.speed))
            else:
                break







    def setEncode(self):
        html =  urllib.urlopen(self.host).read()
        patter = re.compile('charset=utf-8',re.S)
        result = re.findall(patter,html)
        if result and len(result) > 0:
            self.site_charset = "utf-8"
        else:
            self.site_charset = "gbk"

    def islogin(self):
        html =  self.opener.open(urllib2.Request(self.host)).read().decode(self.site_charset)
        if self.username in html:
            return True
        else:
            return False


    def login(self):
        data = {
            "quickforward": "yes",
            "handlekey": "ls",
            "username": self.username,
            "password": self.pwd
        }
        # urllib进行编码。
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
        print result.read().decode(self.site_charset)
        return opener
    def getFormhash(self):
        topic_url = "%s/thread-%s-1-1.html" %(self.host,self.tid)
        xx = self.opener.open(urllib2.Request(topic_url))
        topic_html = xx.read()
        if self.formhash == False:
            pattern = re.compile('<input type="hidden" name="formhash" value="(.*?)" />', re.S)
            formhashs = re.findall(pattern, topic_html)
            if formhashs:
                for item in formhashs:
                    self.formhash = item
                    print(u"表单formhash = %s" % item)  # 901ec69e
                    break  # 找到了就停止循环
            # 未找到则返回
            if not self.formhash:
                print(u'获取formhash失败')
        else:
            print(u"formhash已经初始化过了。%s" % self.formhash)
    def getFid(self):

        if self.fid:
            print(u"fid已经初始化过了。%s" % self.fid)
            return
        topic_url = "%s/thread-%s-1-1.html" %(self.host,self.tid)
        xx = self.opener.open(urllib2.Request(topic_url))
        topic_html = xx.read()
        pattern2 = re.compile('<form.*?id="fastpostform" action="(.*?)"*?</form>', re.S)
        result2 = re.findall(pattern2, topic_html)
        # 从页面中获取fid_url
        if result2:
            fid_url = result2[0]
        if fid_url:  # 匹配到fid_url。则进入解析。
            # 解析fid
            result3 = urlparse.urlparse(fid_url)
            if result3.query == "":
                print(u'没有获取到fid')
            else:
                params3 = urlparse.parse_qs(result3.query, True)
                self.fid = params3['fid'][0]
        # 没有fid ,则返回
        if not self.fid:
             print(u'没有获取到fid')
        print(u"解析的fid = %s " % self.fid)
        pass

    def reply(self):
        self.count = self.count +1
        msg = random.choice(self.msgs)
        reply_url = self.host+"/forum.php?mod=post&action=reply&fid="+self.fid+"&tid="+self.tid+"&extra=page\%3D1&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1"
        headers = {
           # "Referer": "http://bbs.168hs.com/forum.php?mod=post&action=newthread&fid=159",
            "Host": self.host[7:],
        }
        data={
            "formhash":self.formhash,
            "posttime":time.time(),
            "message":msg.encode(self.site_charset)
        }
        #urllib进行编码。
        post_data = urllib.urlencode(data)
        req3 = urllib2.Request(reply_url,post_data,headers)
        rs = self.opener.open(req3)
        ht = rs.read().decode(self.site_charset).lower()
        # print(rs.read().decode(self.site_charset).lower())
        m = re.findall(r'(\w*[0-9]+)\w*',ht)
        print ''.join(m)
        if self.tid in ''.join(m):
            print u'成功'
            self.status = u"成功"
        else:
            print u'失败'
            self.status = u"失败"
        pass


if __name__ == '__main__':
    pass