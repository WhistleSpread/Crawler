from bs4 import BeautifulSoup
import requests
import time
#  不要那么频繁的访问，每次发起一次请求后就停一秒；
import pymongo
#pymongo是python的和mongodb建立连接的一个库；
# 我们将抓取回来的数据放在mongodb这个非关系型数据库里，所以，在抓取数据之前需要先建立数据库；

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

#  通过调用pymongo这个库的MongoClient方法，使python和mongodb建立连接；
client = pymongo.MongoClient('localhost', 27017)
# 你还可以这样 client = MongoClient(“mongodb://localhost:27017/”)

#  这里的client是可以操作的对象；可以利用client 建立一个名字叫做test的数据库，database
#  左边的test是在python 里面操作的对象，右边方括号里面的是在mongodb中数据库的名字；
#  一般来讲，这两个我们一般取得名字是一样的；
test = client['test']


#  在test这个数据库中创建一个名字叫做url_list的表table，因为一个数据库database里面有多个table
#  其实在mongodb中，一个table也被称为是一个collection；
#  同样的，在这里，左边是在python中操作的对象，右边方括号里面是mongodb中创建的表的名字；
url_list = test['url_list']

# 同理，在test这个数据库里创建一个collection，也就是一个table，名字叫做item_info，我们将要把详情页里面
#  每个item的详细信息都放在这张表里面；
item_info = test['item_info']


def get_links_from(channel, pages, who_sells=0):
	"""爬取所有产品页面的链接"""
	# python format 格式化函数 ，最后输出list_view类似: http://bj.58.com/shouji/0/pn3/
	list_view = '{}{}/pn{}/'.format(channel, str(who_sells), str(pages))
	wb_data = requests.get(list_view, headers=headers)
	time.sleep(1)
	soup = BeautifulSoup(wb_data.text, 'lxml')
	# find(name, attrs, recursive, text, **kwargs)
	if soup.find('td', 't'):
		# 表示找到样式t的td标签；
		for link in soup.select('td.t a.t'):
			# select css 选择器，找到所有的 class 为t的td标签下的，class 为t的a标签
			item_link = link.get('href').split('?')[0]
			url_list.insert_one({'url':item_link})
			print(item_link)
	else:
		pass


# 从数据库中取回每一个产品详情页的链接；在获取了详情页的信息之后，从详情页中提取我们需要的数据；
# 从详情页中，我们需要：标题、现价、区域
def get_item_info(url):

	wb_data = requests.get(url)
	soup = BeautifulSoup(wb_data.text, 'lxml')
	title = soup.title.text
	price = soup.select('span[class="price_now"] > i')[0].string
	area = soup.select('div[class="palce_li"] > span > i')[0].string
	item_info.insert_one({'title':title, 'price':price,  'area':area})
	print ({'title':title, 'price':price,  'area':area})




# url = 'http://zhuanzhuan.58.com/detail/1017555639117742090z.shtml'
url = 'http://item.zhuanzhuan.com/1017636778182394376z.shtml'
get_item_info(url)

# no_longer_exists = '404' in soup.find('script', type='text/javascript').get('src').split('/')


# get_links_from('http://bj.58.com/shuma/', 2)


















