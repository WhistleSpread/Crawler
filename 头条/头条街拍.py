#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 16:06:09 2018

@author: gongmike
"""
from urllib import urlencode
from requests.exceptions import RequestException
import requests

def get_page_index(offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload':'true',
        'count':'20',
        'cur_tab': 1
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    response = requests.get(url)
    try:
        
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print '请求索引页失败'
        return None
    
def parse_page_index(html):
    data = json.loads(html)
    

def main():
    html = get_page_index(20, '街拍')
    print 'html =', html

if __name__ == '__main__':
    main()

#######################################################################

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 14:47:54 2018

@author: gongmike
"""


#分析Ajax请求，并抓取今日头条街拍美图
#
#通过ajax加载，并且通过js渲染生成的；
#request+BeautifulSoup+re
#存储的数据库用到mongodb，要用到pymongo这个库；
#
#目标站点分析：
#www.toutiao.com
#有的是组图，有的是单页图（所有的图片都在单个页面中呈现出来；）这次要抓取的是一些组图的形式；
#在图集这个选项中，这里面都是图集的形式；
#查看一下浏览器的源代码；
#chrome 浏览器中network 选项卡中 勾选preserve log（有什么用？）
#然后刷新一下，刷行完之后，网页自动跳到了综合
#可以看到它一般没有返回的html数据，数据一般是通过ajax加载的，
#点击XHR选项，可以看到有一个get形式的请求，
#在header里面，请求的参数后offset，format，keyword
#在preview里面，data中，展开，和title里面的一致；然后url，结尾是2660，
#说明，现在整个网页是通过ajax后台返回的json数据，然后渲染出来的；
#点击图集后，你会发现又出现了一个ajax，看一下preview中的data，看一下title是否对应；
#如果不断下拉的话，后台会出现持续不断的ajax请求，可以看到offset的变化；？offset=20 60 40 80 等；
#其他的参数都是相同的autoload=true, count=20,所以，只要改变offset的值，就可以拿到其他的数据；
#通过访问url，把这些参数改变一下，通过改变offset这个值，拿到不同的数据；
#通过循环，就可以拿到整个街拍组图的数据；
#后台返回的都是一些json数据；拿到后台返回的数据之后，只需要用json的包来解析一下就好；
#
#下面分析，每一个页面的街拍美图；
#点进一个组图之后，查看网页的源代码，打开network，勾选preserve log，刷新一下，看看网页是怎样请求的；
#会不会也是ajax来加载的呢？切换到all，刷新，找到最原始的url请求，也就是文件类型是document，（不过
#为什么我的加载不出来返回结果？不知道？）反正根据教程中说的，返回中没有想要的html代码，然后下面的是js，并没有
#什么有效的信息；推测是不是从ajax来加载的呢？清空信息，然后xhr，
#可以看一下最原始的请求，doc，
#这些数据是在原始请求文档的js里面，然后是以变量的形式来加载的；就是一个gallary变量，要做的就是把这个gallary变量解析
#出来就好了；这个gallary变量不是隐藏在html里的，就不能用beautifulSoup，pyquery这种解析库；
#用正则解析一下就好了；
#
#流程框架：
#抓取索引页的内容，通过ajax，构造ajax请求，把参数传递过来，得到网页的html代码，返回结果即可；
#抓取详情页的内容，通过ajax，返回的json，解析出来的一些文章列表，然后进一步请求url，
#分析gallary变量，然后解析出图片，
#最后把图片下载下来，把图片的名称，原始的url，这些信息都下载下来，然后保存到mongodb中，
#最后开启一个循环，把所有的索引页，通过改变offset，然后把所有的索引页抓取下来；

from urllib import urlencode
from requests.exceptions import RequestException
import requests
import json
import BeautifulSoup
import re
from config import *
from hashlib import md5

# 声明一个mongodb的对象
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
# 上面就定义了一个mongodb对象；

import random
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

# 因为是get形式的请求，参数传递过来就好；
# 将可变的参数作为形式参数传递进来
def get_page_index(offset, keyword):
    data = {
        'offset':offset,
        'format':'json',
        'keyword':'keyword',
        'autoload':'true',
        'count':'20',
        'cur_tab':'3',
    }
    # urlencode 可以把字典对象转化成请求参数；urllib库提供的一个编码方法，因为是get方法，最后
    #的呈现是 https://www.toutiao.com/search_content/?offset=0&format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&cur_tab=3&from=gallery
    #
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    # 然后利用requests来请求这个url
    response = requests.get(url, headers=headers)
    
    # 判断一下返回的状态码，如果返回的状态码是200 则返回成功，只需要把返回的结果打印出来即可；
    try:
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print '请求索引页失败'
        return None

# 对数据进行解析，看看它里面到底是些什么内容
# 返回的是json数据，要对数据进行解析
def parse_page_index(html):
    # 利用json.loads 将json字符串转换成json变量；
    # 因为当前的html是字符串的形式，通过loads 转换成json格式的对象；
    data = json.loads(html)
    
    # 对于索引页面，只需要拿到 详情页的url即可；也就是json对象中的 article_url 提取出来即可；然后
    # 整个的以列表的形式返回就好了；
    # 首先要加一个判断，要保证json数据是含有data这个属性的；然后对data遍历，
    # 这里data.keys()返回所有的键名
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')
            

# 得到了索引页的url，就可以进一步的请求详情页的url了；
# 拿到详情页的组图信息

def get_page_detail(url):
    
    response = requests.get(url, headers=headers)
    # 判断一下返回的状态码，如果返回的状态码是200 则返回成功，只需要把返回的结果打印出来即可；
    try:
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print '请求详情页失败'
        return None
    
def parse_page_detail(html):
    # 因为要提取名称，所以，用BeautifulSoup解析，获得title；传入html，解析方式为lxml
    soup = BeautifulSoup(html, 'lxml')
    # 用Css选择器，用get_text()获取标签里面的文本；
    title = soup.select('title')[0].get_text()
    print 'title =', title
    # 接下来就是提取json串；
    images_pattern = re.compile('var gallery = (.*?);', re.S)
    result = re.search(img_pattern, html)
    if result :
        # 这里得到的是json字符串，需要用json.loads()将其转换成json对象；
#        print 'result.group(1)', result.group(1)
        data = json.loads(result.group(1))
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_imgs')

# 定义一个存储到mongodb的方法； 方法的参数就用一个字典的形式；上面的字典传递过来就好；
def save_to_mongo(result):
    # 加入一个判断，如果插入数据库成功的话，就返回一个true，否则返回False
    if db[MONGO_TABLE].insert(result):
        print '存储到mongodb成功！'， result
        return True
    return False

def download_image(url):
    
    response = requests.get(url, headers=headers)
    # 判断一下返回的状态码，如果返回的状态码是200 则返回成功，只需要把返回的结果打印出来即可；
    try:
        if response.status_code == 200:
            # content 返回的是二进制内容，text 返回的是网页的正常显示结果；正常请求网页的话返回text，如果是图片，就返回content；
            save_image(response.content)
            return response.text
        return None
    except RequestException:
        print '请求图片失败'
        return None

# 包括 路径，名称， 后缀；用format构造一个字符串；路径就是当前文件的路径，名称就是根据文件写的一个名称，后缀就是jpg
def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest，'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close

def main():
    html = get_page_index(0, '街拍')
    print 'html =', html
    # 调用生成器，提取所有的article_url
    for url in parse_page_index(html):
#        print 'url =', url
        print 'url =', 'http://toutiao.com/group/' + str(url)[-19:]
        # 将得到的每个单个的组图索引页的url传入，得到详情页的页面信息！
        html = get_page_detail(url)
        if html:
            parse_page_detail(url)
            save_to_mongo(result)


# 最后对main函数进行循环即可；要获取所有的索引页面，只需要改变一下offset的值就好了；
# 在mongodb中定义一个起始点和终止点，
# 从第一组循环到20组，每组20个；将组数乘20，就可以构造 offset值了；
           
            
if __name__ == '__main__':
    print 'is here'
    main()
    groups = [x*20 for x in range(GROUP_START, GROUP_END + 1)]
    
    
    

# 将数据存储到mongodb中，需要重新建立一个配置文件 config.py
# 将一些配置信息放到文件当中


开启多进程，引入进程池，from multiprocessing import Pool
最后，声明一个进程池 
pool = Pool()
# 利用pool map方法， 开启一下多进程，参数是要执行的目标元素；以及参数的集合，当前的list
pool.map(main, groups)


##################################################################

from urllib import urlencode
import requests
from hashlib import md5
import json
import BeautifulSoup
import os

import random
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

def get_page_index(offset, keyword):
    data = {
        "offset" : '0',
        "format" : 'json',
        "keyword" : 'keyword',
        "autoload" : 'true',
        "count" : '20',
        "cur_tab" : '3',            
    }
    
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    response = requests.get(url, headers=headers)
    return response.text

def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')

def parse_page_detail(html, url):
    # 获得详情页每张图片的url,并下载下来；
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    return {
      'title' : title
      'images' : images
            }
    

def download_images(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest(),'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)

def main():
    html = get_page_index(0, '街拍')
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            result = parse_page_detail(html, url)
            
      