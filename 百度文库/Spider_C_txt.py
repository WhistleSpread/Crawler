import re
import json
import requests

# url = 'https://wenku.baidu.com/view/b1de17e7763231126edb11fa.html?from=search'
# url = 'https://wenku.baidu.com/view/5b3d0ef8b9d528ea81c779f6.html?from=search'
# url = 'https://wenku.baidu.com/view/a7167211abea998fcc22bcd126fff705cc175cac.html?rec_flag=default&sxts=1533957451953'
url = 'https://wenku.baidu.com/view/9d4231d87f1922791688e85e.html?rec_flag=default&sxts=1533957836200'
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}
response = requests.get(url, headers = headers)
source_html = response.content.decode('gbk')
title = re.search(r"title>(.*?)</title>", source_html).group(1)

# with open('Spider_C_txt_'+ title + '.txt', 'w') as f:
# 	f.write(source_html)

docId = re.findall(r"docId: '(.*?)',", source_html)[0]
# print(docId)
token_url = "https://wenku.baidu.com/api/doc/getdocinfo?callback=cb&doc_id=" + (docId)
# print(token_url)
parse_json = requests.get(token_url, headers=headers)
str_first_json = re.match(r".*?\(({.*?})\)", parse_json.text).group(1)
# with open('Spider_C_txt_token_url'+'.json', 'w', encoding='utf-8') as f:
# 	f.write(str_first_json)
init_json = json.loads(str_first_json)
md5sum = init_json["md5sum"]
rn = init_json["docInfo"]["totalPageNum"]
rsign = init_json["rsign"]
target_url = "https://wkretype.bdimg.com/retype/text/"+docId+"?"+md5sum+"&callback=cb"+"&pn=1&rn="+rn+"&type=txt"+"&rsign="+rsign
# print('target_url =', target_url)
str_sec_json = requests.get(target_url)
str_sec_json = re.match(r'.*?\(\[(.*?)\]\)$', str_sec_json.text).group(1)
# with open('Spider_C_txt_str_sec_json'+'.txt', 'w', encoding='UTF-8') as f:
# 	f.write(str_sec_json)
texts=re.findall(r".*?\"c\"\:\"(.*?)\",",str_sec_json)
# print(texts)
for text in texts:
	text = text.encode('latin-1').decode('unicode_escape')
	# print(text)
	with open('Spider_C_txt_' + title + '.txt', 'a') as f:
		f.write(text)



























