#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 15:01:42 2018

@author: gongmike
"""

import re
from re import *
#from re import findall, search, S

secrete_code = 'jsodigixxIxxoaisjgoij239058xxlovexxiowr498t03499xxyouxx9qeu9'

#.的使用
#a = 'xz123'
#b = re.findall('x.', a)
#print b
#可见，点号.是一个占位符，几个点就表示几个符号；

#*的使用
#a = 'xyxy123'
#b = re.findall('x*', a)
#print b


#?的使用
#a = 'xy123'
#b = re.findall('x?', a)
#print b

#在爬虫中，使用正则表达式，其实只需要掌握一种（.*?）这一种组合方式即可；
#b = re.findall('xx.*xx', secrete_code)
#print b
#.# 贪心算法，能找多少找多少；尽可能多的

#c = re.findall('xx.*?xx', secrete_code)
#print c
# .*? 非贪心算法，尽可能的少

# 使用括号，可以将数据作为结果返回
# 需要的内容放在括号里面，不需要的内容放在括号外面；
#d = re.findall('xx(.*?)xx', secrete_code)
#print d
#for each in d:
#    print each


#s = '''josigjxxhello
#xxjosgjsogjxxworldxxjgoji'''
#e = re.findall('xx(.*?)xx', s, re.S)
# 如果没有re.S,那么第一行无法匹配，第一行的内容丢失了；所以从第二行开始；
#print e

#对比findall 与 search的区别：
#s = 'jsodigixxIxx123xxlovexx123xxyouxx9qeu9'
#f = re.search('xx(.*?)xx123xx(.*?)xx123xx(.*?)xx', s).group(1)
# group 是从1开始的，group返回的是括号里的内容；
#print f
# 如果确定只有一个内容时，使用search方法可以提高效率；

#f2 = re.findall('xx(.*?)xx123xx(.*?)xx123xx(.*?)xx', s)
# 因为findall 返回的是一个list，findall，遇到了括号的时候就是这样使用的；
# 除非在string当中，有多个满足xx(.*?)xx123xx(.*?)xx123xx(.*?)xx 这个特征，才有可能 list中有多个元素；
#print 'f2 =', f2
#print f2[0][1]

# sub的使用 sub = substitute
#s = '123jdgoigsj9esg123'
#首先在s中寻找到符合'123(.*?)123'的内容，然后和后面的字符串替换；
#output = re.sub('123(.*?)123', '123789123', s)
#output = re.sub('123(.*?)123', '123%d123'%789, s)
#print output


# 用sub实现翻页的功能
#for i in range(2, total_page+1):
#    new_link = re.sub('pageNum=\d+', 'pageNum=%d'%i, old_url, re.S)
#    print new_link

# 不推荐使用re.compile,原因是如用compile，程序自己会compile一次，所以这里是多此一举；
# 所以不推荐；
#pattern = 'xx(.*?)xx'
#new_pattern = re.compile(pattern, re.S)
#output = re.findall(new_pattern, secrete_code)
#print output

# 匹配纯数字
a = 'gejg9jgoij1241325iogjsi'
b = re.findall('(\d+)', a)
print b











