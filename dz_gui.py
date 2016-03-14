#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: hiphp
@license: Apache Licence 
@contact: hi_php@163.com
@site: wuwenfu.cn
@software: PyCharm Community Edition
@file: hf_gui.py
@time: 2016/3/12 11:48
"""
import wx
import dz_reply
import threading
import time
import thread

import Queue

# isExit = False #退出按钮


flag = False #开关。


def func():
    pass


class Main():
    def __init__(self):
        pass


class MainWindow(wx.Frame):
    '''定义一个窗口类'''

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(600, 700))

        self.myqueue = Queue.Queue(maxsize = 10)

        self.objs ={}

        self.isStop = False #是否停止。
        self.isExit = False



        self.sinal = False

        self.setupContent()

        self.setupMenuBar()
        self.Show(True)

    def setupMenuBar(self):
        self.CreateStatusBar()

        menubar = wx.MenuBar()
        menufile = wx.Menu()

        mnuabout = menufile.Append(wx.ID_ABOUT, u'&关于', u'软件简介')
        mnuexit = menufile.Append(wx.ID_EXIT, u'&退出', u'退出软件')

        menubar.Append(menufile, u'&选项')

        # 事件绑定
        self.Bind(wx.EVT_MENU, self.onAbout, mnuabout)
        self.Bind(wx.EVT_MENU, self.onExit, mnuexit)

        #窗口关闭事件。
        self.Bind(wx.EVT_CLOSE,self.OnClose)


        self.SetMenuBar(menubar)

    def onAbout(self, evt):
        '''点击about的事件响应'''
        dlg = wx.MessageDialog(self, u'针对采用discuzz开发的论坛，可以实现帖子置顶功能。\r\n作者:吴文付 hi_php@163.com', u'关于', wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def onExit(self, evt):
        '''点击退出'''
        self.isExit = True
        self.Close(True)
    def OnClose(self, evt):
        ret = wx.MessageBox(u'你确定要退出软件?',  'Confirm', wx.OK|wx.CANCEL)
        if ret == wx.OK:
            # do something here...
            self.isExit = True
            evt.Skip()


    def setupContent(self):
        panel = wx.Panel(self, -1)

        topLbl = wx.StaticText(panel, -1, u"论坛置顶工具")#1 创建窗口部件
        topLbl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.objs['top'] = topLbl

        siteLabel = wx.StaticText(panel, -1, u"站点域名:")
        # siteText = wx.TextCtrl(panel, -1, "http://bbs.luanren.com",size=(400,-1))
        # siteText.Enable(False)

        sampleList = ['http://bbs.luanren.com', 'http://bbs.chizhouren.com']

        listBox = wx.ListBox(panel, -1, (20, 20), (400, -1), sampleList,
                wx.LB_SINGLE)
        listBox.SetSelection(0)

        siteText = listBox
        self.objs['host'] = siteText

        usernameLabel = wx.StaticText(panel, -1, u"账号:")
        usernameText = wx.TextCtrl(panel, -1, "saoli")

        self.objs['username'] = usernameText


        pwdLabel = wx.StaticText(panel, -1, u"密码:")
        pwdText = wx.TextCtrl(panel, -1, "saoli123")

        self.objs['pwd'] = pwdText



        topicLabel = wx.StaticText(panel, -1, u"帖子编号(tid):")
        topicText = wx.TextCtrl(panel, -1,"5607365")

        self.objs['tid'] = topicText


        speedLabel = wx.StaticText(panel, -1, u"时间间隔(秒):")
        speedText = wx.TextCtrl(panel, -1, "720")

        self.objs['speed'] = speedText

        #状态区
        msgLabel =  wx.TextCtrl(panel,-1,u"针对采用discuzz开发的论坛，可以实现帖子置顶功能。暂定支持bbs.luanren.com，后期会陆续增加更多的支持。作者:吴文付 hi_php@163.com",style=wx.TE_MULTILINE|wx.TE_READONLY,size=(500,220))

        self.objs['msg'] = msgLabel

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topLbl, 0, wx.ALL, 5)
        mainSizer.Add(wx.StaticLine(panel), 0,
                wx.EXPAND|wx.TOP|wx.BOTTOM, 5)

        configSizer  = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)

        configSizer.Add(siteLabel, 0,
                wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        configSizer.Add(siteText, 0, wx.EXPAND)
        # configSizer.Add(listBox, 0, wx.EXPAND)



        configSizer.Add(usernameLabel, 0,
                wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        configSizer.Add(usernameText, 0, wx.EXPAND)

        configSizer.Add(pwdLabel, 0,
                wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        configSizer.Add(pwdText, 0, wx.EXPAND)

        configSizer.Add(topicLabel, 0,
                wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        configSizer.Add(topicText, 0, wx.EXPAND)

        configSizer.Add(speedLabel, 0,
                wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        configSizer.Add(speedText, 0, wx.EXPAND)




        mainSizer.Add(configSizer, 0, wx.EXPAND|wx.ALL, 10)


        mainSizer.Add(msgLabel,0,wx.EXPAND)

        startBtn = wx.Button(panel, -1, u"启动")
        self.startBtn = startBtn
        cancelBtn = wx.Button(panel, -1, u"停止")
        cancelBtn.Disable()
        self.cancelBtn = cancelBtn

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add((20,20), 1)
        btnSizer.Add(startBtn)
        btnSizer.Add((20,20), 1)
        btnSizer.Add(cancelBtn)
        btnSizer.Add((20,20), 1)
        mainSizer.Add(btnSizer, 0, wx.EXPAND|wx.BOTTOM, 10)

        panel.SetSizer(mainSizer)

        self.Bind(wx.EVT_BUTTON, self.onStart, startBtn)
        self.Bind(wx.EVT_BUTTON, self.onStop, cancelBtn)

    def checkValue(self):
        # self.host = self.objs['host'].GetValue()
        self.host = self.objs['host'].GetStringSelection()
        self.objs['msg'].AppendText(u'网站地址:%s\n' % self.host);


        self.username = self.objs['username'].GetValue()
        self.objs['msg'].AppendText(u'账号:%s\n' % self.username);

        self.pwd = self.objs['pwd'].GetValue()
        self.objs['msg'].AppendText(u'密码:%s\n' % self.pwd);

        self.tid = self.objs['tid'].GetValue()
        self.objs['msg'].AppendText(u'帖子编号:%s\n' % self.tid);

        self.speed = self.objs['speed'].GetValue()
        self.objs['msg'].AppendText(u'回帖速度:%s秒\n'% self.speed);

        try:
            self.msgs = getReplylist()
        except Exception,e:
            self.objs['msg'].AppendText(u'读取回帖列表出现异常:%s.\n' % e);
            return
        self.msgs = getReplylist()

        self.objs['msg'].AppendText(u'回帖列表(随机取一条回帖)...\n');
        i = 0
        for msg in self.msgs:
            i = i+1
            self.objs['msg'].AppendText(u'%d.%s\n' %(i,msg));
        self.objs['msg'].AppendText(u'------------------------------------------------\n');



    def replyTopic(self):


        # print(u'启动了')
        self.objs['msg'].AppendText(u'\n获取参数...\n');
        self.checkValue()
        self.msgs = getReplylist()
        # self.msgs = [
        #     u'不错，支持一下.......',
        #     u'已阅，顶一下.......',
        #     u'顶一个...........',
        #     u'路过帮顶........',
        #     u'沙发，沙发.....',
        #     u'我的沙发........',
        #     u'我来了.........',
        #     u'沙发是我的......',
        #     u'我来看看.......',
        #     u'前排，前排........'
        # ]
        print self.msgs

        replyobj =  dz_reply.dz_reply(self.host,self.username,self.pwd,self.tid,self.speed,self.msgs)
        if replyobj.islogin():
            self.objs['msg'].AppendText(u'登录成功...\n')
        else:
            self.objs['msg'].AppendText(u'登录失败...\n')

        replyobj.getFormhash()
        self.objs['msg'].AppendText(u'解析formhash:%s\n' % replyobj.formhash)
        replyobj.getFid()
        self.objs['msg'].AppendText(u'解析fid:%s\n' % replyobj.fid)

        while True:
            if self.isStop:
                self.objs['msg'].AppendText(u'你停止了程序')
                self.objs['msg'].AppendText(u'------------------------------------------------\n');
                return
            replyobj.reply()
            self.objs['msg'].AppendText(u'第%s次回帖:%s' % (replyobj.count,replyobj.status))
            self.objs['msg'].AppendText(u'等待:%s秒\n' % self.speed)
            # thread
            for i in xrange(int(self.speed)):
                #rugu
                if not self.isStop:
                    time.sleep(1)
                else:
                    return
            # time.sleep(float(self.speed))



    def onStop(self,evt):

        self.startBtn.Enable()
        self.cancelBtn.Disable()

        self.isStop = True

        if self.sinal and self.sinal.isSet():
            self.sinal.clear() #设置信号为假的
        self.objs['msg'].AppendText(u'程序停止');

    def onStart(self,evt):


        self.startBtn.Disable() #按钮变灰。

        self.cancelBtn.Enable() #启用按钮

        self.objs['msg'].AppendText(u'\n获取参数...\n');
        self.checkValue()


        # print self.msgs
        # exit()
        # self.msgs = [
        #     u'不错，支持一下.......',
        #     u'已阅，顶一下.......',
        #     u'顶一个...........',
        #     u'路过帮顶........',
        #     u'沙发，沙发.....',
        #     u'我的沙发........',
        #     u'我来了.........',
        #     u'沙发是我的......',
        #     u'我来看看.......',
        #     u'前排，前排........'
        # ]
        # replyobj =  dz_reply.dz_reply(self.host,self.username,self.pwd,self.tid,self.speed,self.msgs)

        self.sinal = threading.Event()
        t = dz_reply.dz_reply(self.myqueue,"回复线程1",self.sinal,self.host,self.username,self.pwd,self.tid,self.speed,self.msgs)
        t.start()

        self.sinal.set()




def updateInfo(frame):
    while True:
        #如果退出了。
        if frame.isExit:
            break;
        if not frame.myqueue.empty():
            frame.objs['msg'].AppendText(frame.myqueue.get())

#获取txt中的内容
def getReplylist():
    result=[]
    with open('replylist.txt','r') as f:
        for line in f:
            result.append(line.decode("utf-8").replace("\n",""))
        return result


def main():
    # global isExit
    app = wx.App(False)
    frame = MainWindow(None, u'论坛工具')
    thread.start_new_thread(updateInfo,(frame,))
    app.MainLoop() #循环监听事






if __name__ == '__main__':
    main()
    # thread.start_new_thread(main,())
    # pass11