#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: hiphp
@license: Apache Licence 
@contact: hi_php@163.com
@site: wuwenfu.cn
@software: PyCharm Community Edition
@file: tidytest.py
@time: 2016/2/29 16:59
"""
from subprocess import Popen,PIPE

#2016年2月29日 失败，安装tidy非常麻烦。资料很少。

def tidytest():
    text = open("errormsg.html").read()
    tidy = Popen('tidy',stdin=PIPE,stdout=PIPE,stderr=PIPE)

    tidy.stdin.write(text)
    tidy.stdin.close()

    print tidy.stdout.read()

    pass


class Main():
    def __init__(self):
        pass


if __name__ == '__main__':
    tidytest()
    pass