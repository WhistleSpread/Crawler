import requests
import re
import json
import os

session = requests.session()
def fetch_url(url):
    return session.get(url).content.decode('gbk')
def get_doc_id(url):
    return re.findall('view/(.*).html', url)[0]
def parse_type(content):
    return re.findall(r"docType.*?\:.*?\'(.*?)\'\,", content)[0]
def parse_title(content):
    return re.findall(r"title.*?\:.*?\'(.*?)\'\,", content)[0]

def parse_txt(doc_id):
    content_url = 'https://wenku.baidu.com/api/doc/getdocinfo?callback=cb&doc_id=' + doc_id
    content = fetch_url(content_url)
    md5 = re.findall('"md5sum":"(.*?)"', content)[0]
    pn = re.findall('"totalPageNum":"(.*?)"', content)[0]
    rsign = re.findall('"rsign":"(.*?)"', content)[0]
    content_url = 'https://wkretype.bdimg.com/retype/text/' + doc_id + '?rn=' + pn + '&type=txt' + md5 + '&rsign=' + rsign
    content = json.loads(fetch_url(content_url))
    result = ''
    for item in content:
        for i in item['parags']:
            result += i['c'].replace('\\r', '\r').replace('\\n', '\n')
    return result

def save_file(filename, content):
    with open(filename, 'w', encoding='utf8') as f:
        f.write(content)
        print('已保存为:' + filename)
        
# test_txt_url = 'https://wenku.baidu.com/view/cbb4af8b783e0912a3162a89.html?from=search'
# test_ppt_url = 'https://wenku.baidu.com/view/2b7046e3f78a6529657d5376.html?from=search'
# test_pdf_url = 'https://wenku.baidu.com/view/dd6e15c1227916888586d795.html?from=search'
# test_xls_url = 'https://wenku.baidu.com/view/eb4a5bb7312b3169a551a481.html?from=search'

def main():
    url = input('请输入要下载的文库URL地址')
    content = fetch_url(url)
    doc_id = get_doc_id(url)
    type = parse_type(content)
    title = parse_title(content)
    if type == 'doc':
        result = parse_doc(content)
        save_file(title + '.txt', result)
    elif type == 'txt':
        result = parse_txt(doc_id)
        save_file(title + '.txt', result)
    else:
        parse_other(doc_id)
if __name__ == "__main__":
    main()
