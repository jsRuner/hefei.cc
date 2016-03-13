#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: hiphp
@license: Apache Licence 
@contact: hi_php@163.com
@site: wuwenfu.cn
@software: PyCharm Community Edition
@file: main.py
@time: 2016/2/29 19:11
"""

import time

import wx



def main():
    app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
    frame = wx.Frame(None, wx.ID_ANY, "Hello World") # A Frame is a top-level window.
    frame.Show(True)     # Show the frame.
    app.MainLoop()
    pass


class Main():
    def __init__(self):
        pass


if __name__ == '__main__':
    main()
    pass