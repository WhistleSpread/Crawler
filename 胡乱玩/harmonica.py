#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 17:46:28 2018

@author: gongmike
"""

# 爬取学口琴音乐网的简谱 http://www.xuekouqin.com

import requests
from bs4 import BeautifulSoup
import chardet

path = '/Users/gongmike/Desktop/pics/'
url = 'http://www.xuekouqin.com/yuepu/jd/index.html'


def get_one_score_url(scores_url):
    html = requests.get(scores_url)
    bsop = BeautifulSoup(html.text, 'lxml')
    url = 'http://www.xuekouqin.com' + bsop.select('body > div > div > div > div.kqjp_art')[0].img.get('src')
    return url


response = requests.get(url).text
response.encode('utf8','ignore')   
print response
print 'response =', chardet.detect(response)
print type(response)
bsop = BeautifulSoup(response, 'lxml')
scores_list = bsop.select('body > div.w100.pt5 > div.kqjp_list > div.jp_lt_d > ul > li > h3')

for item in scores_list:
    href = 'http://www.xuekouqin.com' + item.a.get('href')
    title = item.a.get_text()
#    print 'title =', title
#    print type(title)
    item_url = get_one_score_url(href)
    img_html = requests.get(item_url) 
    with open(path + title, 'wb') as f:
        f.write(img_html.content)
    

get_one_score_url('http://www.xuekouqin.com/yuepu/29.html')
