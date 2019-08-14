'''
思路：通过加入爬虫头headers，kv = {'User-agent': 'Baiduspider'}
模拟百度爬虫robot，这个是被允许访问的；来实现百度文库word、txt的爬取

'''



import requests
from bs4 import BeautifulSoup
import bs4

def getHTMLText(url):
    kv = {'User-agent': 'Baiduspider'}
    try:
        r = requests.get(url, headers = kv, timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''

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
    printPList(plist, title)


# url = 'https://wenku.baidu.com/view/d0bfc6f0f90f76c661371a68.html'\
url = 'https://wenku.baidu.com/view/7f08a898580216fc710afd29.html?from=search'

Spider_1(url)















