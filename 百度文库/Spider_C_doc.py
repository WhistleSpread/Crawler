import re
import json
import requests


# url = 'https://wenku.baidu.com/view/d0bfc6f0f90f76c661371a68.html'
url = 'https://wenku.baidu.com/view/7f08a898580216fc710afd29.html?from=search'
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
    print(url + '\n\n\n')
# print(direct_url_lists)

result = ''
for url in direct_url_lists:
	content = requests.get(url).content.decode()
	content = re.match(r'.*?\((.*)\)$', content).group(1)
	all_body_info = json.loads(content)["body"]
	print(all_body_info)
	y_tmp = ''
	ps_enter = None
	for body_info in all_body_info:
		try:

			if body_info["ps"]["_enter"] == 1:
				result += '\n' + text_result
			else:
				result += text_tesult
		except KeyError:
			pass
	    # text_result = body_info["c"]
	    # if y_tmp == body_info["p"].get('y'):
	    #     result += text_result
	    # else:
	    #     result += '\n' + text_result
	    #     y_tmp = body_info["p"].get('y')

print(result)
with open('Spider_C_doc_result'+ title + '.txt', 'w') as f:
	f.write(result)


