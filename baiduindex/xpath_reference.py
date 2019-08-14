from lxml import etree

Selector = etree.HTML

Selector.xpath(一段神奇的符号)

# 如何利用XPath来提取内容
# // 是定位根节点
# / 是往下层寻找
# 如果想要提取文本内容： /text()
# 如果想要提取属性内容： /@xxxx

from lxml import etree
import requests

html = requests.get(url)
selector = etree.HTML(html)

#提取文本
content = selector.xpath('//ul[@id='useful']/li/text()')
# 因为id是独一无二的，所以可以直接在根节点下这样找；
# 其实只要在根节点下找到独一无二的既可以；
for each in content:
    print each
# 提取属性
link = selector.xpath('//a/@href')
# 这里是提取在根节点下，所有的a标签的href的属性
for each in link:
    print each
title = selector.xpath('//a/@title')
# 提取在根节点下所有a标签的属性为title的a标签；
print title[0]
# 因为返回的是一个列表；