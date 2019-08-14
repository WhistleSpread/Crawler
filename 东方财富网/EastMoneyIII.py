import requests
from bs4 import BeautifulSoup
import random
import json
from lxml import etree

UserAgent_List = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
headers = {'User-Agent': random.choice(UserAgent_List),
           'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           'Accept-Encoding': 'gzip',
           }


output = open('data.xls','a+',encoding='gbk')
output.write("姓名\t性别\t年龄\t学历\t职务\n")
output.close()

url = "http://quote.eastmoney.com/stocklist.html"
html = requests.get(url, headers=headers)
html.encoding = html.apparent_encoding

selector = etree.HTML(html.text)
content = selector.xpath('//ul/li/a/@href')
stockname = selector.xpath('//ul/li/a/text()')
stockname = stockname[59:-22]

urlList = []
codeList = []

for item in content:
    if(item[0:12] == 'http://quote'):
        urlList.append(item)
        codeList.append(item[-13:-5])

urlList = urlList[16:-1]
codeList = codeList[16:-1]
code = zip(codeList, stockname)

# for item in code:
#     print('item = ', item[0])

baseurl = 'http://emweb.securities.eastmoney.com/PC_HSF10/CompanyManagement/CompanyManagementAjax?code='
for stock in code:
    # print('code[0] = ', item[0])
    url = baseurl + stock[0]
    # print('url = ', url)    
    html = requests.get(url, headers=headers).text
    response = json.loads(html)
    RptManagerList = response.get("Result").get("RptManagerList")
    item_num = len(RptManagerList)
    print('item_num = ', item_num)
    # output = open('data.xls','a+',encoding='gbk')
    # output.write("姓名\t性别\t年龄\t学历\t职务\n")
    # output.close()
    for item in RptManagerList:
        cd = stock[0]
        name = stock[1]
        xm = item.get("xm")
        xb = item.get("xb")
        nl = item.get("nl")
        xl = item.get("xl")
        zw = item.get("zw")
        itemline = (cd, name, xm, xb, nl, xl, zw)
        output = open('data.xls','a+',encoding='gbk')
        for item in itemline:
            try:
                output.write(str(item))
                output.write('\t')
            except UnicodeEncodeError:
                pass
        output.write('\n')
        output.close()
        print('done one!')






