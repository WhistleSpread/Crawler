import requests
import re
import argparse
import sys
import json
import os


parser = argparse.ArgumentParser()
parser.add_argument("url", help="Target Url,你所需要文档的URL",type=str)
parser.add_argument('type', help="Target Type,你所需要文档的的类型(DOC|PPT|TXT|PDF)",type=str)
args = parser.parse_args()

url = args.url
type = args.type

#根据文件决定函数
y = 0
def DOC(url):
    doc_id = re.findall('view/(.*).html', url)[0]
    html = requests.get(url).text
    lists=re.findall('(https.*?0.json.*?)\\\\x22}',html)
    lenth = (len(lists)//2)
    NewLists = lists[:lenth]
    for i in range(len(NewLists)) :
        NewLists[i] = NewLists[i].replace('\\','')
        txts=requests.get(NewLists[i]).text
        txtlists = re.findall('"c":"(.*?)".*?"y":(.*?),',txts)
        for i in range(0,len(txtlists)):
            global y
            print(txtlists[i][0].encode('utf-8').decode('unicode_escape','ignore'))
            if y != txtlists[i][1]:
                y = txtlists[i][1]
                n = '\n'
            else:
                n = ''
            filename = doc_id + '.txt'
            with open(filename,'a',encoding='utf-8') as f:
                f.write(n+txtlists[i][0].encode('utf-8').decode('unicode_escape','ignore').replace('\\',''))
        print("文档保存在"+filename)


if __name__ == "__main__":
    try:
        print("""TIPS:PDF|PPT只能下载图片""")
        eval(type.upper())(url)
    except:
        print("获取出错，可能URL错误\n使用格式name.exe url type\n请使用--help查看帮助")
