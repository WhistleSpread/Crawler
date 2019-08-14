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

def TXT(url):
    doc_id = re.findall('view/(.*).html', url)[0]
    url = "https://wenku.baidu.com/api/doc/getdocinfo?callback=cb&doc_id="+doc_id
    html = requests.get(url).text
    md5 = re.findall('"md5sum":"(.*?)"',html)[0]
    pn = re.findall('"totalPageNum":"(.*?)"',html)[0]
    rsign = re.findall('"rsign":"(.*?)"',html)[0]
    NewUrl = 'https://wkretype.bdimg.com/retype/text/'+doc_id+'?rn='+pn+'&type=txt'+md5+'&rsign='+rsign
    txt = requests.get(NewUrl).text
    jsons = json.loads(txt)
    texts=re.findall("'c': '(.*?)',",str(jsons))
    print(texts)
    filename=doc_id+'.txt'
    with open(filename,'a',encoding='utf-8') as f:
        for i in range(0,len(texts)):
            texts[i] = texts[i].replace('\\r','\r')
            texts[i] = texts[i].replace('\\n','\n')

            f.write(texts[i])
    print("文档保存在" + filename)


if __name__ == "__main__":
	eval(type.upper())(url)
