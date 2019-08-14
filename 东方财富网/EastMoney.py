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


url = "http://quote.eastmoney.com/stocklist.html"
html = requests.get(url, headers=headers)
html.encoding = html.apparent_encoding

selector = etree.HTML(html.text)
content = selector.xpath('//ul/li/a/@href')
# print("len_of_content = ", len(content))

urlList = []

# print(html)
for item in content:
    # print("item = ", item)
    with open('sz_stock_symbol.txt', 'a+') as f:
        f.write(str(item)+'\n')
    if(item[0:12] == 'http://quote'):
        urlList.append(item)
urlList = urlList[15:-1]

# print('urlList = ', urlList)
for i in urlList:
    print('item = ',i)

print(len(urlList))
# with open('sz_stock_symbol.txt', 'w') as f:
#     f.write(html.text)

# html = html.text
# soup = BeautifulSoup(html, 'lxml')
# soup = BeautifulSoup(open('sz_stock_symbol.html')) 
# result = soup.find_all("div", class_="sltit")
# result = soup.select("#quotesearch > ul > li > a")
# result = soup.find_all("a", href=re.compile("quote"))
# print("content = ", content)




# url = "http://emweb.securities.eastmoney.com/PC_HSF10/CompanyManagement/CompanyManagementAjax?code=SZ000006"
# html = requests.get(url, headers=headers).text
# response = json.loads(html)

# print("Result = ", response)
# print(type(response))
# print(response.keys())
# print(response.get("Result"))
# print(type(response.get("Result")))
# print(response.get("Result").keys())
# print(response.get("Result").get("RptManagerList"))

# RptManagerList = response.get("Result").get("RptManagerList")

# print(RptManagerList)

# item_num = len(RptManagerList)
# output = open('data.xls','a+',encoding='gbk')
# output.write("姓名\t性别\t年龄\t学历\t职务\n")
# output.close()
# for item in RptManagerList:
#     xm = item.get("xm")
#     xb = item.get("xb")
#     nl = item.get("nl")
#     xl = item.get("xl")
#     zw = item.get("zw")
#     itemline = (xm, xb, nl, xl, zw)
#     output = open('data.xls','a+',encoding='gbk')
#     for item in itemline:
#         output.write(str(item))
#         output.write('\t')
#     output.write('\n')
#     output.close()


































