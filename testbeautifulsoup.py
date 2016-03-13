#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: hiphp
@license: Apache Licence 
@contact: hi_php@163.com
@site: wuwenfu.cn
@software: PyCharm Community Edition
@file: testbeautifulsoup.py
@time: 2016/2/29 17:18
"""

from urllib import urlopen

# from BeautifulSoupTests import BeautifulSoup
from bs4 import  BeautifulSoup,BeautifulStoneSoup



def testbeautifulsoup():
    text = urlopen("http://info.sporttery.cn/football/search_odds.php").read()
    soup = BeautifulSoup(text,'lxml')

    # print soup


    # print soup.select("#match_team > a")

    footballs = set()

    for match in soup.select("#match_team > a"):

        for string in match.strings:
            print string
        # print match.strings

        # footballs.add("%s" % )



    pass


class Main():
    def __init__(self):
        pass


if __name__ == '__main__':
    testbeautifulsoup()
    pass