import requests
from bs4 import BeautifulSoup
import bs4

url = 'https://wenku.baidu.com/view/d0bfc6f0f90f76c661371a68.html'

headers = {'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'}
html = requests.get(url, headers=headers)
html.encoding = html.apparent_encoding
with open('Spider_A_two_html.txt', 'w') as f:
    f.write(html.text)

kv = {'User-agent': 'Baiduspider'}
html = requests.get(url, headers = kv, timeout = 30)
r.encoding = r.apparent_encoding
with open('Spider_A_simRobot_html.txt', 'w') as f:
    f.write(r.text)



def findPList(html):
    plist = []
    soup = BeautifulSoup(html, "html.parser")
    plist.append(soup.title.string)
    for div in soup.find_all('div', attrs={"class": "bd doc-reader"}):
        plist.extend(div.get_text().split('\n'))

    plist = [c.replace(' ', '') for c in plist]
    plist = [c.replace('\x0c', '') for c in plist]
    return plist

def printPList(plist,title):
    path = './data/' + title + '.txt'
    file = open(path, 'w')
    for str in plist:
        file.write(str)
        file.write('\n')
    file.close()

def Spider_1(url):
    html = getHTMLText(url)
    plist = findPList(html)
    title = plist[0]
    writeFile(title, html)
    # printPList(plist, title)



