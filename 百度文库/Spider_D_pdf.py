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




def PDF(url):
    doc_id = re.findall('view/(.*).html',url)[0]
    url = "https://wenku.baidu.com/browse/getbcsurl?doc_id="+doc_id+"&pn=1&rn=99999&type=ppt"
    html = requests.get(url).text
    lists=re.findall('{"zoom":"(.*?)","page"',html)
    for i in range(0,len(lists)):
        lists[i] = lists[i].replace("\\",'')
    try:
        os.mkdir(doc_id)
    except:
        pass
    for i in range(0,len(lists)):
        img=requests.get(lists[i]).content
        with open(doc_id+'\img'+str(i)+'.jpg','wb') as m:
            m.write(img)
    print("FPD图片保存在" + doc_id + "文件夹")


if __name__ == "__main__":
    try:
        print("""
###Athor:Lz1y
###Blog:www.Lz1y.cn
###TIPS:PDF|PPT只能下载图片
        """)
        eval(type.upper())(url)
    except:
        print("获取出错，可能URL错误\n使用格式name.exe url type\n请使用--help查看帮助")