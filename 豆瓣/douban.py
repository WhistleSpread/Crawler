#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 16:25:10 2018

@author: gongmike
"""

#!/usr/bin/env python
# encoding: utf-8
import time
import requests
import random
from lxml import etree
# 把str编码由ascii改为utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')


headers = [
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
    {'User-Agent': 'Mozilla/5.0 (compatiblemztfix; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
    {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
]


def main():
    tags = ['哲学', '计算机', '心理学', '生活', '数学']

    fileContent = ''  # 最终要写到文件里的内容，这个算是在生成的txt文件打上一个时间戳？
    fileContent += '生成时间：' + time.asctime() #time.asctime()函数接受时间元组并返回一个可读的形式为"Tue Dec 11 18:07:14 2008"
    print 'time.asctime()= ', time.asctime() # 奇怪，为什么这个没有打印出来？难道没有执行？
    
    
    for tag in tags:
        fileContent += bookSpider(tag)
        print "%s down!" % tag

    with open('book_list.txt', 'w') as f:
        f.write(fileContent)


def bookSpider(bookTag):
    result = '' # 这里保存的是下载下来的结果
    divide = '\n' + '--' * 30 + '\n' + '--' * 30 + '\n' # 这里打印的分割线，打印了两行；
    result += divide + '\t' * 4 + bookTag + '：' + divide # 首先是分割线，下一行是4个tab，然后是标签名称，tab是为了让标签处于中间，然后又是分割线；

    url = "http://www.douban.com/tag/%s/book" % bookTag  # 其实现在的url变成了：https://book.douban.com/心理
    global headers 
    html = requests.get(url, headers=random.choice(headers)).content
    print html
    tree = etree.HTML(html.decode('utf-8')) # 这里用到了lxml中的etree方法
    print'tree =', tree
    books = tree.xpath("//dl/dd")
    print 'books = ', books

    count = 1
    for book in books:
        # 得到书名
        title = book.xpath("a/text()")[0].strip()
        # 得到出版信息
        desc = book.xpath("div[@class='desc']/text()")[0].strip() # strip()的作用是去除首尾空格；
        descL = desc.split('/') # 按 ‘/’ 进行分割；得到一个包含所有信息的list；
        authorInfo = '作者/译者： ' + '/'.join(descL[:-3]) # 从左边到倒数第4个；
        pubInfo = '出版信息： ' + '/'.join(descL[-3:]) #从倒数第3个一直到最后；
        # 得到评分
        rating = book.xpath("div/span[@class='rating_nums']/text()")[0].strip()
        # 加入结果字符串
        result += "*%d\t《%s》\t评分：%s\n\t%s\n\t%s\n\n" % (count, title, rating, authorInfo, pubInfo)

        count += 1

    return result


if __name__ == "__main__":
    main()
    #  bookSpider('哲学')
    
#######################################################################
import requests, random
from requests.exceptions import RequestException
import re
import json
from io import open


# 构造headers
# 设置userAgent 起到隐藏身份的作用，用户代理ua；将ua存放在header中，因为服务器通过header中的ua来判断睡在访问
#Python允许我们修改这个User Agent来模拟浏览器访问
UserAgent_List = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
headers = {'User-Agent': random.choice(UserAgent_List),
           'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           'Accept-Encoding': 'gzip',
           }


def get_one_page(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print 'status_code = 200'
            return response.text
        else:
            return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<a.*?title="(.*?)".*?pub">(.*?)</div>.*?rating_nums">(.*?)</span>')
    items = re.findall(pattern, html) # findall 返回匹配对象的list
    print 'items=', items
    for item in items:
        yield {
            'title':item[0],
            'pub':item[1],
            'rating':item[2],
        }
        
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close
        
def main(start):
    url = 'https://book.douban.com/tag/经济学?start='+ str(start) + '&type=T'
    html = get_one_page(url)
    print 'html =', html
    parse_one_page(html)
    for item in parse_one_page(html):
        print 'item =', item
        write_to_file(item)

if __name__ == '__main__':
    for i in range(10):
        main(i*10)
