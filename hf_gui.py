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


def func():
    pass


class Main():
    def __init__(self):
        pass


class MainWindow(wx.Frame):
    '''定义一个窗口类'''

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(600, 600))
        # self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)

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

        self.SetMenuBar(menubar)

    def onAbout(self, evt):
        '''点击about的事件响应'''
        dlg = wx.MessageDialog(self, u'针对采用discuzz开发的论坛，可以实现帖子置顶功能。\r\n作者:吴文付 hi_php@163.com', u'关于', wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def onExit(self, evt):
        '''点击退出'''
        self.Close(True)

    def setupContent(self):
        panel = wx.Panel(self, -1)

        topLbl = wx.StaticText(panel, -1, u"论坛置顶工具")#1 创建窗口部件
        topLbl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))

        siteLabel = wx.StaticText(panel, -1, u"站点域名:")
        siteText = wx.TextCtrl(panel, -1, "http://baidu.com",size=(400,-1))

        usernameLabel = wx.StaticText(panel, -1, u"账号:")
        usernameText = wx.TextCtrl(panel, -1, "saoli")


        pwdLabel = wx.StaticText(panel, -1, u"密码:")
        pwdText = wx.TextCtrl(panel, -1, "saoli123")



        topicLabel = wx.StaticText(panel, -1, u"帖子编号(tid):")
        topicText = wx.TextCtrl(panel, -1,"")


        speedLabel = wx.StaticText(panel, -1, u"时间间隔(秒):")
        speedText = wx.TextCtrl(panel, -1, "720")

        #状态区
        msgLabel =  wx.TextCtrl(panel,-1,u"工具准备ok！",style=wx.TE_MULTILINE|wx.TE_READONLY,size=(500,220))
        # mutiRightStr="Example again\n But this time\nWe Align Right!"
        # msgLabel = wx.StaticText(panel,-1,mutiRightStr,(500,220))



        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topLbl, 0, wx.ALL, 5)
        mainSizer.Add(wx.StaticLine(panel), 0,
                wx.EXPAND|wx.TOP|wx.BOTTOM, 5)

        configSizer  = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)

        configSizer.Add(siteLabel, 0,
                wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        configSizer.Add(siteText, 0, wx.EXPAND)
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

        saveBtn = wx.Button(panel, -1, u"启动")
        cancelBtn = wx.Button(panel, -1, u"停止")

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add((20,20), 1)
        btnSizer.Add(saveBtn)
        btnSizer.Add((20,20), 1)
        btnSizer.Add(cancelBtn)
        btnSizer.Add((20,20), 1)
        mainSizer.Add(btnSizer, 0, wx.EXPAND|wx.BOTTOM, 10)

        panel.SetSizer(mainSizer)


def main():
    app = wx.App(False)
    frame = MainWindow(None, u'论坛工具')
    app.MainLoop() #循环监听事



if __name__ == '__main__':
    main()
    pass