#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 17:49:35 2018

@author: gongmike
"""
import requests
import re


# 创建Beautiful Soup 对象，需要导入bs4库
from bs4 import BeautifulSoup

url = 'http://news.qq.com'
# 关于requests库还要看看，每次写都忘记加上text；
# text方法，可以将返回的unicode编码的html；
response = requests.get(url).text
print 'response =', response
print type(response) # <type 'unicode'>

# 创建一个beautifulsoup对象
soup = BeautifulSoup(response)
print 'soup =', soup
print type(soup)
# 可以看到 类型为 <class 'bs4.BeautifulSoup'>

 # 用本地文件创建bs对象
soup = BeautifulSoup(open('index.html'))  

 # 打印soup对象的内容
print soup.prettify()

 # 关于tag，soup.tag 查找所在内容中的第一个符合要求的标签，如果要查询所有标签，可以用select；
print soup.title
print soup.a
print soup.p
print soup.head

 # 这些对象的类型是bs4中的tag对象，BeautifulSoup将复杂的html转换成树形结构，每个节点
 # 都是python对象，所有对象可以归纳为4种：tag、navigablestring、beautifulsoup、comment
print type(soup.title)
print type(soup.a)
print type(soup.p)
print type(soup.head)

# 对于tag，它有2个重要的属性，name和attrs；
print soup.title.name
print soup.a.name
print soup.p.name
print soup.head.name
 # 对于一般的内部标签，name获得的值就是标签本身的名字；比较特殊的是soup的名字[document]
print soup.name

 # 关于attrs，attrs，就是把所有的属性，以字典的形式返回出来；
print soup.title.attrs
print soup.a.attrs
print soup.p.attrs
print soup.head.attrs

 # 如果要获取某个属性的值，直接访问属性名，就可以输出属性值；
print soup.a['accesskey']
print soup.a['href']

 # 也可以用get方法，传入属性名称，两种方法等价；
print soup.a.get('target')
print soup.a.get('style')

 # 对于这些属性也可以修改，删除，不过这些都不是我们的主要用途；

 # NavigableString
 # 得到了标签的内容后，想要得到标签内部的文字，用.string方法即可；不过，这个是可遍历的字符串NavigableString类型
print soup.p.string
print type(soup.p.string)

 # 接下来讲一下遍历文档树的操作：
 # 直接的子节点 .contents 和 .children 属性；
 # tag的 .content 属性可以将tag的子节点以list的形式输出
print soup.title.contents
print soup.a.contents
print soup.p.contents 
print soup.head.contents 
print soup.head.contents[1]

# tag 的.children 方法，它返回的不是一个list，可以通过遍历获取所有的子节点；

print soup.head.children
print type(soup.head.children)
 # 打印出来可以看到它是一个list生成器对象；
 # <listiterator object at 0x112267150>
 # <type 'listiterator'>
 # 要获得生成器里面的内容，遍历一下即可；
for child in soup.head.children:
    print child
    print

 # 所有子孙节点 用.descendants
 # .content 和 .children 属性仅仅包含tag的直接子节点，.descendants 属性可以对所有的tag的
 # 子孙节点进行递归循环，和children 类似，类型也是一个生成器；
print soup.descendants
print type(soup.descendants)
# <generator object descendants at 0x110075c30>
# <type 'generator'>
for child in soup.descendants:
    print child

# 节点内容。如果一个标签里面没有标签了，那么 .string 就会返回标签里面的内容。
# 如果标签里面只有唯一的一个标签了，那么 .string 也会返回最里面的内容
# 但是，如果如果 tag 包含了多个子节点,tag 就无法确定，string 方法应该调用哪个子节点的内容, .string 的输出结果是 None
print soup.title.string
print soup.a.string
print soup.p.string
print soup.head.string
print soup.html.string


# 要获取多个内容，可以使用.strings 或者 .stripped_strings（可以除去多余空白内容）
print soup.html.strings
# 打印出来的是一个生成器，需要用遍历获取；
# <generator object _all_strings at 0x112628690>
for string in soup.html.strings:
    print string

# 输出的字符串中可能包含了很多空格或空行,使用 .stripped_strings 可以去除多余空白内容
for string in soup.html.stripped_strings:
    print string   

# 用.parents 属性可以属性可以得到父节点
p = soup.p
print p.parent.name
head = soup.head
print head.parent.name

#  用.parents 属性可以递归得到元素的所有父辈节点，得到的是一个生成器，需要遍历得到元素；
# content = soup.head.title.string
print content
print type(content)
for parent in  content.parents:
    print parent.name  
    
 # 还有其他的需要详细看的：兄弟节点、全部兄弟节点、前后节点、所有前后节点等；


# 搜索文档树
# find_all(name, attrs, recursive, text, **kwargs)
# 搜索当前tag的所有tag子节点，并判断是否符合过滤器的条件；
# find_all() 方法返回全部的搜索结构,如果文档树很大那么搜索会很慢.
# 如果我们不需要全部结果,可以使用 limit 参数限制返回结果的数量.效果与 SQL 中的 limit 关键字类似,
# 当搜索到的结果数量达到 limit 的限制时,就停止搜索返回结果.
#  name 参数可以查找所有名字为 ‘name’ 的 tag；
print soup.find_all('b')
print soup.find_all('a')
print soup.find_all('img')
print soup.find_all('br')

 # 除了传入字符串，也可以传入正则表达式，Beautiful Soup 会通过正则表达式的 match() 来匹配内容
 # 下面例子中找出所有以b开头的标签
import re
#print soup.find_all(re.compile("^b"))
for tag in soup.find_all(re.compile("^b")):
    print(tag.name)
 
# 传列表
# 如果传入列表参数,Beautiful Soup 会将与列表中任一元素匹配的内容返回.
# 下面代码找到文档中所有 <a> 标签和 <b> 标签
print soup.find_all(["a", "b"])

  
# 传入 Ture， True 可以匹配任何值,下面代码查找到所有的tag,但是不会返回字符串节点
for tag in soup.find_all(True):
    print(tag.name)

#  如果没有合适的过滤器，那么还可以定义一个函数方法，
# 方法只接受一个元素参数如果这个方法返回 True 表示当前元素匹配并且被找到,如果不是则反回 False
def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')
#  现将这个定义好了的方法传入find_all()方法中，将得到所有的具有class，可是没有id的标签；
# soup.find_all(has_class_but_no_id)

 # 如果一个指定名字的参数不是搜索内置的参数名，搜索时，会把该参数当作指定名字tag的属性来搜索；
 # 如果包含一个名字为id的参数，bs会搜索每个tag的id属性；
 # 因为find_all方法，是所有的都要找到，所以，搜索到速度会相当的慢；
 # 按照id搜索
print soup.find_all(id='link2')
 # 如果传入 href 参数,Beautiful Soup 会搜索每个 tag 的 ”href” 属性
print soup.find_all(href=re.compile("elsie"))
 # 可以使用多个指定名字的参数可以同时过滤 tag 的多个属性
print soup.find_all(href=re.compile("elsie"), id='link1')
 # 在这里我们想用 class 过滤，不过 class 是 python 的关键词，这怎么办？加个下划线就可以
print soup.find_all("a", class_="sister")
 # 有些 tag 属性在搜索不能使用,比如 HTML5 中的 data-* 属性
 # 但是可以按照attr来搜索,可以定义字典来搜索包含特殊属性的tag；
soup.find_all(attrs={'data-foo':'value'})

# 通过 text 参数可以搜索文档中的字符串内容.
#  与 name 参数的可选值一样, text 参数接受 字符串 , 正则表达式 , 列表, True


soup.find_all(text="Elsie")
soup.find_all(text=["Tillie", "Elsie", "Lacie"])
soup.find_all(text=re.compile("Dormouse"))

# find_all() 方法返回全部的搜索结构,如果文档树很大那么搜索会很慢.
# 如果我们不需要全部结果,可以使用 limit 参数限制返回结果的数量.
# 效果与 SQL 中的 limit 关键字类似,当搜索到的结果数量达到 limit 的限制时,就停止搜索返回结果.
soup.find_all("a", limit=2)


# 调用 tag 的 find_all() 方法时,
# Beautiful Soup 会检索当前 tag 的所有子孙节点,
# 如果只想搜索 tag 的直接子节点,可以使用参数 recursive=False .
soup.html.find_all("title", recursive=False)

 find(name, attrs , recursive , text , **kwargs )
# 它与 find_all() 方法唯一的区别是 find_all() 方法的返回结果是值包含一个元素的列表,而 find() 方法直接返回结果
#  检索的都是tag，所以，这两个返回的结果也是一样的；为了找到BeautifulSoup对象内任何第一个标签入口，使用find()方法
#  find就是找到第一次出现的那个标签的bs对象；find_all()是找到所有具有这个标签的bs对象；
print soup.head
print soup.find('head')



 # CSS选择器
 # 我们在写 CSS 时，标签名不加任何修饰，类名前加点，id名前加 #，
 # 在这里我们也可以利用类似的方法来筛选元素，用到的方法是 soup.select()，返回类型是 list

 # 通过标签名查找   
print soup.select('title') 
print soup.title.string
print soup.select('a')
print soup.select('b')

# 通过类名查找
print soup.select('.Q-tpList')

 # 通过id名查找
print soup.select('#subHot')

 # 组合查找：
 # 和写 class 文件时，标签名与类名、id 名进行的组合原理是一样的，
 # 例如查找 p 标签中，id 等于 link1 的内容，二者需要用空格分开
print soup.select('p #link1')
 # 或者直接子标签查找
print soup.select("head > title")
# 这里用selcet 可以看到有的标签查找子标签是用的，空格，有的使用的 > 
# > 表示严格的下一级的子元素，空格 表示所有的子孙元素；

#  属性查找
# 查找时还可以加入属性元素，属性需要用中括号括起来，
# 注意属性和标签属于同一节点，所以中间不能加空格，否则会无法匹配到。
 print soup.select('a[class="sister"]')
 print soup.select('a[href="http://example.com/elsie"]')

 # 属性仍然可以与上述查找方式组合，不在同一节点的空格隔开，同一节点的不加空格
 print soup.select('p a[href="http://example.com/elsie"]')
 # 表示找到p节点下面的 属性有href属性为"http://example.com/elsie"的所有a标签；


