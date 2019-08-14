import re
import json
import requests


url = 'https://wenku.baidu.com/view/4210c1661fb91a37f111f18583d049649b660e0c.html?from=search'
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}
response = requests.get(url, headers = headers)
source_html = response.content.decode('gbk')
title = re.search(r"title>(.*?)</title>", source_html).group(1)

with open('Spider_C_pdf_source_html'+'.html', 'w') as f:
	f.write(source_html)

url_list = list()
all_url_lists = re.findall(r'wkbjbos\.bdimg\.com.*?json.*?expire.*?\}',source_html)
print(all_url_lists)

for url in all_url_lists:
	url = url.replace("\\\\\\/", '/')
	url = 'https://' + url
	url = url[:-5]
	print(url + '\n\n\n')
 #    url = "https://" + url.replace("\\\\\\/", "/")
 #    print(url)
 #    url = url[:-5]
 #    all_url_lists.append(url)
    # print(url + '\n\n\n')

# result = ''
# for url in all_url_lists:
# 	content = requests.get(pure_addr).content.decode()
# 	content = re.match(r'.*?\((.*)\)$', content).group(1)
# 	all_body_info = json.loads(content)["body"]
# 	# print(all_body_info)
# 	y_tmp = ''
# 	for body_info in all_body_info:
# 	    text_result = body_info["c"]
# 	    if y_tmp == body_info["p"].get('y'):
# 	        result += text_result
# 	    else:
# 	        result += '\n' + text_result
# 	        y_tmp = body_info["p"].get('y')

# # print(result)
# with open('Spider_C_pdf_result'+ title + '.txt', 'w') as f:
# 	f.write(result)
