# 因为需要长时间的爬取，如果存在一点错误的话，程序就暂停了；
# 报错停止耽误时间；
# 可以用try except，出现这个错误就跳过；
# try excetp

def try_to_make(a_mess):
	try:
		print(1/a_mess)
	except ZeroDivisionError:
		print('我知道是你用0作为分母了，sb')

try_to_make(0)

# 有一个比较有意思的 东西
'area':list(map(lambda x:x.text), soup.select('ul.det-info > li:nth-of-type[3] > a'))
# 这里的lambda和map都很有意思 这里的soup返回的的是一个list；
# python中的map函数，存在2个参数，左边参数是一个函数，右边是list_of_inputs 可以是一个list，也可以是tuple什么的；
# map 会将一个函数映射到一个输入列表的所有元素上；这样就不需要一个一个的将值传递给函数，这样可以一次性的计算出来；
# 大多数的时候，map都配合lambda 这个匿名函数来一起完成任务；

#  关于zip和 enumerate；
# zip() 函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表。
# 如果各个迭代器的元素个数不一致，则返回列表长度与最短的对象相同，利用 * 号操作符，可以将元组解压为列表。
# 与 zip 相反，*zipped 可理解为解压，返回二维矩阵式

import requests
from bs4 import BeautifulSoup
url 

soup = BeautifulSoup(wbdata.text, 'lxml')
imgs = soup.select('selector1')
titles = soup.select('selector2')
links = soup.select('selector3')

for img, title, link in zip(imgs, titles, links):
    data = {
            'img':img.get('src'),
            'title':title.get('title'),
            'link':link.get('href'),
            },
    #  这里data得到的会是一个元组，这个元组包含三个元素
    print data