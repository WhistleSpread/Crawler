# -*- coding: utf-8 -*-
import requests     # 导入模块
import re
import json
import os
import pymysql
# pip install pymysql
session = requests.session()


def fetch_url(url):        # 获取地址
    return session.get(url).content.decode('gbk')


def get_doc_id(url):       # 获取id
    return re.findall('view/(.*).html', url)[0]


def parse_type(content):     # 获取类型
    return re.findall(r"docType.*?\:.*?\'(.*?)\'\,", content)[0]


def parse_title(content):     # 获取标题
    return re.findall(r"title.*?\:.*?\'(.*?)\'\,", content)[0]


def parse_doc(content):       # 爬取doc格式的文件
    result = ''
    url_list = re.findall('(https.*?0.json.*?)\\\\x22}', content)
    url_list = [addr.replace("\\\\\\/", "/") for addr in url_list]
    for url in url_list[:-5]:
        content = fetch_url(url)
        y = 0
        txtlists = re.findall('"c":"(.*?)".*?"y":(.*?),', content)
        for item in txtlists:
            if not y == item[1]:
                y = item[1]
                n = '\n'
            else:
                n = ''
            result += n
            result += item[0].encode('utf-8').decode('unicode_escape', 'ignore')
    return result



def save_file(filename, content):
    with open(filename, 'w', encoding='utf8') as f:
        f.write(content)
        print('已保存为:' + filename)


	

# test_txt_url = 'https://wenku.baidu.com/view/cbb4af8b783e0912a3162a89.html?from=search'
# test_ppt_url = 'https://wenku.baidu.com/view/2b7046e3f78a6529657d5376.html?from=search'
# test_pdf_url = 'https://wenku.baidu.com/view/dd6e15c1227916888586d795.html?from=search'
# test_xls_url = 'https://wenku.baidu.com/view/eb4a5bb7312b3169a551a481.html?from=search'
# 用于测试的链接
def main():
    url = input('请输入要下载的文库URL地址')       # 爬取url链接中的内容
    content = fetch_url(url)
    doc_id = get_doc_id(url)
    type = parse_type(content)
    title = parse_title(content)
    if type == 'doc':                  # 根据文件的格式保存文件
        result = parse_doc(content)
        save_file(title + '.txt', result)
    elif type == 'txt':
        result = parse_txt(doc_id)
        save_file(title + '.txt', result)
        print(save_mysql(result))     # 将结果输入数据库
    else:
        parse_other(doc_id)


if __name__ == "__main__":
    main()