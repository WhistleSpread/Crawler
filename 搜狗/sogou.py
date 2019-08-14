# 如果状态码是302，那么ip被封了，切换代理，重新请求

import requests
from urllib.parse import urlencode
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq
import pymongo
from config import *




client = pymongo.MongoClient(MONGO_URL)
db = client(MONGO_DB)

base_url = 'http://weixin.sogou.com/weixin?'

headers = {
	'Cookie':'GOTO=Af99047; SUV=00CD592DDAC711C857B900E3ABB97779; CXID=29EDA4FA02ED75E72837D8E44FFAB66A; SUID=C811C7DA4C6C860A57D8D23F000B8144; IPLOC=CN4201; ABTEST=7|1535894058|v1; SNUID=84D9C827545120B667EACB40550FC14D; weixinIndexVisited=1; JSESSIONID=aaa9c3R3OwcIS4zX1OBvw; ppinf=5|1535899935|1537109535|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxMzp3aGlzdGxlc3ByZWFkfGNydDoxMDoxNTM1ODk5OTM1fHJlZm5pY2s6MTM6d2hpc3RsZXNwcmVhZHx1c2VyaWQ6NDQ6bzl0Mmx1THEwbHNkaVpJT3ZHU3pCX3hwT203Z0B3ZWl4aW4uc29odS5jb218; pprdig=TYaIhtZFK3i5gzt0agQkPjjaPXfkLZGQZBnMaRsTtzcAp_ZxJk9rk7n9BF42hhW1QzNhlfMxnXqvPPH6ijoWP2e0xY_j5-eWV_IMRhQZH_sfrGUBoPC6UIYhI7H4_blVWtjnNxOv-TlC1QOaH2NIBefiNRobgyfxqfpSqJAJTLg; sgid=28-36935703-AVuLibRic7Bs96XNJd9hNV8dM; ppmdig=15358999360000000e7cf06e05f12c0f2d4ff691c55aae7b; sct=4',
	'Host':'weixin.sogou.com',
	'Upgrade-Insecure-Requests':'1',
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}



proxy = None






def get_proxy():
	try:
		response = requests.get(PROXY_POOL_URL)
		if response.status_code == 200:
			return response.text
		return None
	except ConnectionError:
		return None

def get_html(url, count=1):
	print('Crawling ', url)
	print('Trying count', count)
	global proxy
	if count >= MAX_COUNT:
		print('Tried too many counts')
		return None
	try:
		if proxy:
			proxies = {
				'http':'http://' + proxy
			}
			response = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies)
			# 加入参数，不要自动的处理跳转，这样才能拿到302状态码；
		else:
			response = requests.get(url, allow_redirects=False, headers=headers)
			# 加入参数，不要自动的处理跳转，这样才能拿到302状态码；

		if response.status_code == 200:
			return response.text
		if response.status_code == 302:
			# Need Proxy
			print('302')
			proxy = get_proxy()
			if proxy:
				print('Using proxy', proxy)
				return(get_html(url))
			else:
				print('Get Proxy Failed')
				return None

	except ConnectionError as e:
		print('error occured', e.args)
		proxy = get_proxy()
		count += 1
		return get_html(url, count)


def get_index(keyword, page):
	data = {
		'query' : keyword,
		'type' : 2,
		'page' : page,
	}

	# 将这个字典用urlencode进行编码，把它转成get请求参数的样子
	queries = urlencode(data)
	url = base_url + queries
	html = get_html(url)
	return html

def parse_index(html):
	doc = pq(html)
	items = doc('.news-box .news-list li .txt-box h3 a').items()
	# 这里使用了items()方法，得到一个生成器
	for item in items:
		yield item.attr('href')

def get_detail(url):
	try:
		response = requests.get(url)
		if response.status_code == 200:
			return response.text
		return None
	except ConnectionError:
		return None

def parse_detail(html):
	doc = pq(html)
	title = doc('.rich_media_title').text()
	content = doc('rich_media_content').text()
	data = doc('#post-data').text()
	nickname = doc('.rich_media_meta_list .rich_media_meta_nickname').text()
	wechat = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
	return {
		'title':title, 
		'content':content,
		'data':data,
		'wechat':wechat,
		'nickname':nickname,
	}

def save_to_mongo(data):
	if db['articles'].update({'title':data['title']}, {'$set', data}, True):
		print('Saved to Mongo', data['title'])
	else:
		print('Saved to Mongo Failed', data['title'])





def main():
	for page in range(1, 101):
		html = get_index(KEYWORD, page)
		if html:
			article_urls = parse_index(html)
			for article_url in article_urls:
				article_html = get_detail(article_url)
				if article_html:
					article_data = parse_detail(article_html)
					save_to_mongo(article_data)

			

if __name__ == '__main__':
	main()





























