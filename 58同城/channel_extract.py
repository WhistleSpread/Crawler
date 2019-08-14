from bs4 import BeautifulSoup
import requests
import random

start_url = 'http://bj.58.com/sale.shtml'
url_host = 'http://bj.58.com'


# http://cn-proxy.com/
#  到这上面去找一些访问速度比较好的代理
#  通过添加代理IP，降低被封的风险；
#  如果一个ip请求过于频繁，网站可能会封ip；

# proxy_list = [
# 	'http://117.177.250.151:0001',
# 	'http://111.85.219.250:3129',
# 	'http://122.70.183.138:8118',
# ]
# proxy_ip = random.choice(proxy_list) # 随机获取代理ip
# proxies = {'http':proxy_ip}


def get_channel_urls(url):
	"""获取各个频道的链接"""
	# wb_data = requests.get(start_url, proxies=proxies)
	wb_data = requests.get(start_url)
	soup = BeautifulSoup(wb_data.text, 'lxml')
	links = soup.select('ul.ym-submnu > li > b > a')
	for link in links:
		page_url = url_host + link.get('href')
		print (page_url)

get_channel_urls(start_url)

# 对于非常长的字符串，我们用三引号

channel_list = '''
	http://bj.58.com/shouji/
	http://bj.58.com/tongxunyw/
	http://bj.58.com/danche/
	http://bj.58.com/diandongche/
	http://bj.58.com/fzixingche/
	http://bj.58.com/sanlunche/
	http://bj.58.com/peijianzhuangbei/
	http://bj.58.com/diannao/
	http://bj.58.com/bijiben/
	http://bj.58.com/pbdn/
	http://bj.58.com/diannaopeijian/
	http://bj.58.com/zhoubianshebei/
	http://bj.58.com/shuma/
	http://bj.58.com/shumaxiangji/
	http://bj.58.com/mpsanmpsi/
	http://bj.58.com/youxiji/
	http://bj.58.com/ershoukongtiao/
	http://bj.58.com/dianshiji/
	http://bj.58.com/xiyiji/
	http://bj.58.com/bingxiang/
	http://bj.58.com/jiadian/
	http://bj.58.com/binggui/
	http://bj.58.com/chuang/
	http://bj.58.com/ershoujiaju/
	http://bj.58.com/yingyou/
	http://bj.58.com/yingeryongpin/
	http://bj.58.com/muyingweiyang/
	http://bj.58.com/muyingtongchuang/
	http://bj.58.com/yunfuyongpin/
	http://bj.58.com/fushi/
	http://bj.58.com/nanzhuang/
	http://bj.58.com/fsxiemao/
	http://bj.58.com/xiangbao/
	http://bj.58.com/meirong/
	http://bj.58.com/yishu/
	http://bj.58.com/shufahuihua/
	http://bj.58.com/zhubaoshipin/
	http://bj.58.com/yuqi/
	http://bj.58.com/tushu/
	http://bj.58.com/tushubook/
	http://bj.58.com/wenti/
	http://bj.58.com/yundongfushi/
	http://bj.58.com/jianshenqixie/
	http://bj.58.com/huju/
	http://bj.58.com/qiulei/
	http://bj.58.com/yueqi/
	http://bj.58.com/kaquan/
	http://bj.58.com/bangongshebei/
	http://bj.58.com/diannaohaocai/
	http://bj.58.com/bangongjiaju/
	http://bj.58.com/ershoushebei/
	http://bj.58.com/chengren/
	http://bj.58.com/nvyongpin/
	http://bj.58.com/qinglvqingqu/
	http://bj.58.com/qingquneiyi/
	http://bj.58.com/chengren/
	http://bj.58.com/xiaoyuan/
	http://bj.58.com/ershouqiugou/
	http://bj.58.com/tiaozao/
	http://bj.58.com/tiaozao/
	http://bj.58.com/tiaozao/
'''

