# -*- coding: UTF-8 -*-
import urllib2, urllib, cookielib, re, time,json
import random
import sqlite3
import threading
import ConfigParser

class Robot:

    def __init__(self, forumUrl, userName, password, proxy = None):

        self.forumUrl = forumUrl
        self.userName = userName
        self.password = password
        self.token = ''
        self.fid = 2497
        self.isLogon = False
        self.formhash=''


        self.jar = cookielib.CookieJar()
        if not proxy:
            openner = urllib2.build_opener(
        urllib2.HTTPCookieProcessor(self.jar))
        else:
            openner = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(self.jar),
            urllib2.ProxyHandler({'http' : proxy}))
        urllib2.install_opener(openner)

    def login(self):
        request = urllib2.Request("http://bbs.duowan.com/api/mobile/?module=login&action=verifycode&version=2")

        request.add_header('Host', 'bbs.duowan.com')
        request.add_header("User_Agent","DuowanBbs_Android/2.0.3_284/6.0/HUAWEI NXT-AL10/6c5cc111-5883-4de8-8c63-2dd7a595fa9b")
        # request.add_header("Cookie","Cookie")
        # request.add_header("Mag-Deviceid","860076030620446")
        # request.add_header("Mag-Mgsc","31d0477d5d506e967a8614b890636905")

        data = {
            "deviceId":"00000000-6de2-6f96-ffff-fffff092bdfb",
            "appToken":"rrBwwTLmIUM9lzZnfwtHT0QIYFo0nVHPJhlAnvsQ9k7ogUzA8UZvIOAagIt+5a8QSNe9xBdjZct3wDKOn/y3whZqZXaKrlFBRFrdEPj8fgo=",
            "yyuid":"75786795",
        }


        data = urllib.urlencode(data)
        # response = urllib.urlopen(request,data)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(request,data)
        content = response.read()
        # print content
        # exit()
        if "45690584" in content:
            self.isLogon = True
            #解析json。
            result = json.loads(content)
            # self.token = result['token']
            print(u"--------------登录信息------------------")
            for item in result.keys():
                if item == "Variables" or item == 'Message':
                    # print result[item].keys()
                    for it in result[item].keys():
                         print "|    %s:%s   " % (it,result[item][it])
                         if it == "formhash":
                             self.formhash = result[item][it]
                    # resultchild = json.loads(result[item])
                    # print resultchild
                    # for itemchild in resultchild.keys():
                    #     print "|    %s:%s   " % (itemchild,resultchild[itemchild])
                else:
                    print "|    %s:%s   " % (item,result[item])
            print(u"--------------登录信息------------------")
            # exit()

            # print 'login success!'
        else:
            pass
            # print 'login faild!'
    #获取主题列表。json.
    def getTids(self):
        # self.token = "7ade721c39fcb6bd9d8da3f28149147c"
        # self.fid = 297
        baselink = "http://newapp.hefei.cc/mv3_bbs_contentlist"
        # link =  "http://newapp.hefei.cc/mv3_bbs_contentlist?step=20&_token="+self.token+"&build=3.1.0&timeline=1455867980&p="+p+"&version=135&fid=297&clienttype=android&"
        data = {
            "step":20,
            "_token":self.token,
            "build":"3.1.0",
            "timeline":int(time.time()),
            "p":1,
            "version":20,
            "fid":self.fid,
            "clienttype":"android",
        }
        link = baselink+"?"+urllib.urlencode(data)
        # print link
        tidPage = urllib2.urlopen(link).read()
        result = json.loads(tidPage)
        # result2 = json.loads(result['list'])
        tids =[]
        for item in result['list']:
            # print item
            # print item['id']
            # result_item = json.loads(item)
            # print result_item['id']
            tids.append(item['id'])
        return tids
    #获取所有板块fid集合
    #http://newapp.hefei.cc/mv3_bbs_grouplist?step=20&_token=7ade721c39fcb6bd9d8da3f28149147c&build=3.1.0&clienttype=android&p=1&version=135&
    def getFids(self):
        baselink = "http://newapp.hefei.cc/mv3_bbs_grouplist"
        data = {
            "step":20,
            "_token":self.token,
            "build":"3.1.0",
            "p":1,
            "version":135,
        }
        link = baselink+"?"+urllib.urlencode(data)
        # print link
        fidPage = urllib2.urlopen(link).read()
        result = json.loads(fidPage)
        fids =[]
        for item in result['data']:
            for item_child in item['_child']:
                # print item_child
                #不存在则插入
                if item_child['id'] not in fids:
                    fids.append(item_child['id'])
        return fids

    def getOneTitle(self):
        result = urllib2.urlopen(self.forumUrl + '/forum.php')
        reglink = r"href=\"(http\:\/\/chizhouren\.com\/forum\.php\?mod=viewthread&tid=6796.+?)\""
        link = re.findall(re.compile(reglink),result.read())
        print link[0]
        return link[0]

    def getTid(self,link):
        tidPage=urllib2.urlopen(link).read()
        tidnum=re.search('\d{6}',link)
        print tidnum.group()
        return tidnum.group()

    def getFid(self,link):
        tidPage=urllib2.urlopen(link).read()
        fid =re.search('<input\s*type="hidden"\s*name="srhfid"\s*value="([\w\W]+?)"\s*\/>',tidPage)
        print fid.group(1)
        return fid.group(1)

    def initFormhashXq(self):
        content = urllib2.urlopen(self.forumUrl + '/plugin.php?id=dsu_paulsign:sign')
        content = content.read()
        rows = re.findall(r'<input\s*type="hidden"\s*name="formhash"\s*value="([\w\W]+?)"\s*\/>', content)
        if len(rows)!=0:
            self.formhash = rows[0]
            print 'formhash is: ' + self.formhash
        else:
            print 'none formhash!'

    def reply(self,tid,msg):

        html = ''
        request = urllib2.Request("http://bbs.duowan.com/api/mobile/?module=sendreply&version=2")
        request.add_header('Host', 'bbs.duowan.com')
        request.add_header('Content-Type', 'multipart/form-data; boundary=YDAkwzi9e85c7qAdLaFImAPqPRjLTI_3')
        request.add_header("User_Agent","DuowanBbs_Android/2.0.3_284/6.0/HUAWEI NXT-AL10/6c5cc111-5883-4de8-8c63-2dd7a595fa9b")
        request.add_header("Cookie","bbs_4477_lastvisit=1457062403; bbs_4477_pc_size_c=0; bbs_4477_ulastactivity=a6bfi5ZnQxCyTYiMHzpXH6cJ0%2FtnWv0%2FugcKLc%2Bv%2FbQNinb%2BfKdu; bbs_4477_forum_lastvisit=D_992_1457066004; bbs_4477_forum_lastpage=992_1; bbs_4477_mobile=no; bbs_4477_lastact=1457066009%09index.php%09viewthread; bbs_4477_fid2497=1457335572; bbs_4477_visitedfid=2497D992; bbs_4477_sid=MpgGim; bbs_4477_auth=6e73vnrq/msY7yIUGpzQgjblY+v/bCNH2nPUV7aNCaoVaLd8LlmJxiYIXh8FpAkWNMGhq7/p8Lbd0IlgXpErtX+ttxY91w; bbs_4477_saltkey=ll12jJBd")
        data = {
            'Content-Disposition: form-data; name="formhash"Content-Type: text/plain; charset=UTF-8Content-Transfer-Encoding: 8bit':"5d1fea8e",
            'Content-Disposition: form-data; name="replysubmit"Content-Type: text/plain; charset=UTF-8Content-Transfer-Encoding: 8bit':"yes",
            'Content-Disposition: form-data; name="tid"Content-Type: text/plain; charset=UTF-8Content-Transfer-Encoding: 8bit':"44316203",
            'Content-Disposition: form-data; name="fid"Content-Type: text/plain; charset=UTF-8Content-Transfer-Encoding: 8bit':"2497",
            'Content-Disposition: form-data; name="message"Content-Type: text/plain; charset=UTF-8Content-Transfer-Encoding: 8bit':"iamtheking",
        }
        print data
        data = urllib.urlencode(data)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(request,data)
        html = response.read().decode("gbk")
        print("%s" % html)
        result  = json.loads(html)
        return result

        print 'reply success!'

#是否到了工作时间
def isstart(start, end):
    xstr = time.strftime('%Y-%m-%d')
    st = xstr + " " + start
    ed = xstr + " " + end

    b = time.time()
    t1 = time.mktime(time.strptime(st, '%Y-%m-%d %H:%M:%S'))

    t2 = time.mktime(time.strptime(ed, '%Y-%m-%d %H:%M:%S'))

    # 小于开始时间，大于结束时间。则为False
    if b < t1 or b > t2:
        return False
    else:
        return True


def loop():
    cf = ConfigParser.ConfigParser()
    cf.read('config.ini')
    username = cf.get("info","username")
    password = cf.get("info","password")
    speed = cf.get("info","speed")
    speed = float(speed)
    robot = Robot('http://bbs.duowan.com', username, password)
    robot.login()
    replylist = getReplylist()
    # replylist = [
    #         u'不错，支持一下.......',
    #         u'已阅，顶一下.......',
    #         u'顶一个...........',
    #         u'路过帮顶........',
    #         u'沙发，沙发.....',
    #         u'我的沙发........',
    #         u'我来了.........',
    #         u'沙发是我的......',
    #         u'我来看看.......',
    #         u'前排，前排........'
    # ]
    time.sleep(2)
    #随机获取一些帖子。进行回复。回复一个，就删除一个。如果回复完了，再次获取。
    # fids = robot.getFids()
    #设置fid
    # while True:
    # temp = random.choice(fids)
    temp = 2497
    robot.fid = temp
    #获取tids
    time.sleep(2)
    # tids = robot.getTids()
    tids = ['44316203']

    tidstr = ",".join(tids)
    print u"随机获取帖子id的集合为:%s" % tidstr

    for item in tids:
        if not isstart("06:00:00", "23:59:59"):
            print(u"未到工作时间")
            time.sleep(30)
        print item
        print u"正在回复:"+"http://bbs.duowan.com/thread-"+item+"-1-1.html"
        content = random.choice(replylist)
        content = content.encode('utf-8')
        print content
        try:
            print "11111"
            result = robot.reply(item,content)
        except Exception,e:
            print(u'回帖发生异常。进入下一步。%' % e)
            time.sleep(30)
            continue

        if not result['success']:
            # print "too quick..."
            print result['msg']
            #睡眠时间延长。
            speed = speed +120
        else:
            data = result['data']
            print(u"--------------回帖信息------------------")
            for item in data.keys():
                print "|    %s:%s   " % (item,data[item])
            print(u"--------------回帖信息------------------")
        #20秒后再回复。
        print(u"等待%s秒后再次操作" % speed)
        time.sleep(speed)
#获取txt中的内容
def getReplylist():
    result=[]
    with open('replylist.txt','r') as f:
        for line in f:
            result.append(line.decode("utf-8").replace("\n",""))
            # print line
        # print(result)
        return result
    # replylist = [
    #         u'不错，支持一下.......',
    #         u'已阅，顶一下.......',
    #         u'顶一个...........',
    #         u'路过帮顶........',
    #         u'沙发，沙发.....',
    #         u'我的沙发........',
    #         u'我来了.........',
    #         u'沙发是我的......',
    #         u'我来看看.......',
    #         u'前排，前排........'
    # ]

    # print replylist

if __name__ == '__main__':
    # getReplylist()
    while True:
        try:
            loop()
        except Exception,e:
            print(u'发现异常,睡眠50秒%s' % e)
            time.sleep(30)

    # cf = ConfigParser.ConfigParser()
    # cf.read('config.ini')
    # username = cf.get("info","username")
    # password = cf.get("info","password")
    # speed = cf.get("info","speed")
    # robot = Robot('http://bbs.hefei.cc', username, password)
    # robot.login()
    # replylist = [
    #         u'不错，支持一下.......',
    #         u'已阅，顶一下.......',
    #         u'顶一个...........',
    #         u'路过帮顶........',
    #         u'沙发，沙发.....',
    #         u'我的沙发........',
    #         u'我来了.........',
    #         u'沙发是我的......',
    #         u'我来看看.......',
    #         u'前排，前排........'
    # ]
    # #随机获取一些帖子。进行回复。回复一个，就删除一个。如果回复完了，再次获取。
    # fids = robot.getFids()
    # #设置fid
    # robot.fid = random.choice(fids)
    # #获取tids
    # tids = robot.getTids()
    # for item in tids:
    #     print item
    #     print "http://bbs.hefei.cc/thread-"+item+"-1-1.html"
    #     content = random.choice(replylist)
    #     content = content.encode('utf-8')
    #     robot.reply(item,content)
    #     #20秒后再回复。
    #     time.sleep(speed)



