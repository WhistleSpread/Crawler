import re
import json
import requests


# url = 'https://wenku.baidu.com/view/d0bfc6f0f90f76c661371a68.html'
# url = 'https://wenku.baidu.com/view/7f08a898580216fc710afd29.html?from=search'
# url = 'https://wenku.baidu.com/view/6b5d452ba0116c175e0e482b.html?sxts=1533964712619'
# url = 'https://wenku.baidu.com/view/f5da030c82c4bb4cf7ec4afe04a1b0717fd5b3e5.html?rec_flag=default&sxts=1533964988622'
# url = 'https://wenku.baidu.com/view/d0bfc6f0f90f76c661371a68.html'
# url = 'https://wenku.baidu.com/view/169a9fb726fff705cd170a1b.html?from=search'
url = 'https://wenku.baidu.com/view/169a9fb726fff705cd170a1b.html?from=search&pn=51'

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}
response = requests.get(url, headers = headers)
source_html = response.content.decode('gbk')
title = re.search(r"title>(.*?)</title>", source_html).group(1)

# with open('Spider_C_doc_'+ title + '.txt', 'w') as f:
# 	f.write(source_html)

direct_url_lists = list()
all_url_lists = re.findall(r'wkbjbos\.bdimg\.com.*?json.*?expire.*?\}',source_html)
# print(all_url_lists)

for url in all_url_lists:
    url = "https://" + url.replace("\\\\\\/", "/")
    url = url[:-5]
    direct_url_lists.append(url)
    # print(url + '\n\n\n')
# print(direct_url_lists)

result = ''
for url in direct_url_lists:
	content = requests.get(url).content.decode()
	content = re.match(r'.*?\((.*)\)$', content).group(1)
	all_body_info = json.loads(content)["body"]
	# print(all_body_info)
	y_tmp = ''
	for body_info in all_body_info:
		# print(body_info['ps']['_enter'])
		# print(type(body_info['ps']))
		if body_info['ps'] is not None:
			try:
				if body_info['ps']['_enter'] == 1:
					# print('Gocha!!!')
					result += '\n'
			except KeyError:
				pass
		else:
			try:

				result += body_info['c']
			except TypeError:
				pass
# print(result)
with open('Spider_C_doc_result'+ title + '.txt', 'a') as f:
	f.write(result)







