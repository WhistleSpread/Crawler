#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 16:42:43 2018

@author: gongmike
"""

# PhantomJs 是一个无界面的浏览器；在页面爬取的时候，开着浏览器非常不方便，
# 使用PhantomJS 可以帮我们更方便的爬取；
# 爬取淘宝美食关键词下的所有宝贝内容；并存储到momgodb
# 解析库是pyquery 

# 目标站点分析www.taobao.com
# 首先模拟在文本框中输入要搜索的关键词
# 然后点击搜索按钮
# 获取首页的内容
# 模拟点击翻页，或者在后面输入翻页；然后获取后面的页面；

#得到网页的源代码之后，分析各个宝贝的信息，然后将信息存储到mongodb数据库；

import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pyquery import PyQuery as pq
from config import *
import pymongo

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

def search():
        
    browser.get('https://www.taobao.com')
    # 要判断加载成功；waits
    # 显式等待；不过这个显式等待我还没有看的太明白；
    input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
    )
    submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
    input.send_keys('美食')
    submit.click()
    
    total = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
    
    get_products()
    return total.text
                                                   
# 模拟翻页的内容，首先需要获取页数；要等待判断，等待页数加载出来；

def next_page(page_num):
    input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
    )
    submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
    input.clear()
    input.send_keys(page_num)
    submit.click()
    
    # 要判断分页是否成功，需要找一下，当前页码的数字是否是当前的数字；
    wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_num)))
    get_products()
    
    
# 可以翻页之后，就解析页码，得到宝贝的信息；
def get_products():
    # 先判定一下这个items是否加载成功；
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    # 如果这里执行通过的话，则表明，所有的宝贝信息都已经加载成功了；
    # 后面要进行的操作是用pyquery来解析一下；
    # 用page_source 方法可以拿到网页的源代码；
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    # 调用items方法，得到所有选择的内容；
    for item in items:
        # 得到每个item之后，就可以分析图片，宝贝信息；
        product = {
            'image' : item.find('.pic .img').attr('src'),
            'price' : item.find('.price').text(),
            'deal' : item.find('.deal-cnt').text()[:-3],
            'title' : item.find('.title').text(),
            'shop' : item.find('.shop').text(),
            'location' : item.find('.location').text(),
        }
        print(product)
        save_to_mongo(product)


# 下一步就是把这些数据保存到mongodb中，
# 需要新建一个配置文件，config.py        
# 定义一个保存到mongodb的方法；

def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('保存成功', result)


def main():
    total = search()
    total = int(re.compile('(\d+)').search(total).group(1))
    
#    print(total)
    for i in range(2, total + 1):
        next_page(i)

if __name__ == '__main__':
    main()
    
    


# 出现一个浏览器太麻烦了，最好是让浏览器不出现，在后台允许，可以用phantomjs
# 可以把chrome 该成phantomjs，如果要用phantomjs的话，要安装phantomjs。
# 相对于chrome来说，phantomjs还有高级的配置；点击api可以看到，有command line的接口；
    