#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 16:40:51 2018

@author: gongmike
"""


# httpbin 是一个测试http请求和响应的网站；
#httpbin 能够测试http请求以及响应等各种信息，比如cookies\ip\headers\和登陆验证
# 等等；支持post\get多种方法，对web的开发和测试有很大帮助，它是用python+Flask编写的；
# 且是一个开源的项目；
# 可以使用httpbin作为测试工具来测试http库，因为httpbin可以cover各类的http场景
# 而且每一个接口一定都有返回；利用httpbin可以测试http请求和响应的各种信息；




import requests

#r = requests.get("http://httpbin.org/get")
#r = requests.post("http://httpbin.org/post")
#r = requests.put("http://httpbin.org/put")
#r = requests.delete("http://httpbin.org/delete")
#r = requests.head("http://httpbin.org/get")
#r = requests.options("http://httpbin.org/get")
#print r
#<Response [200]>
#print type(r)
#<class 'requests.models.Response'>

# 重点讲一下get请求和post请求，以及定制请求头

#使用Requests发送get请求很简单：
#r = requests.get("http://httpbin.org/get")

#有些情况下，url会带有参数，Requests提供了params关键字参数，允许我们以一个字典来提供
#这些参数
#payload ={'page':'1', 'per_page':'10'}
#r = requests.get('http://httpbin.org/get', params=payload)
#print r.url
#可以看到打印出来的已经正确编码了：http://httpbin.org/get?per_page=10&page=1


# 使用requests发送post请求
#r = requests.post('http://httpbin.org/post')
#print r
#通常在发送post请求时，还会附上数据，比如说，发送编码为表单形式，或者编码为json数据
# 可以通过Requests 提供的data参数；

#发送编码为表单形式的数据；
#通过给data参数传递一个dict，数据字典在发出请求时，会被自动编码为表单形式
#payload = {'page':1, 'per_page':10}
#r = requests.post('http://httpbin.org/post', data=payload)
#print r
# 可以用text方法查看返回的内容
#print r.text

# 除了发送编码为表单的形式之外，还可以发送编码为json形式的数据；
#给data参数传递一个string， 我们的数据会被直接发布出去；

# 请求头
#有时候，我们需要为请求添加http头部；可以通过字典给headers传递参数来实现；

#url = 'http://httpbin.org/post'
#payload = {'page':1, 'per_page':10}
#headers = {'User-Agent':'Mozilla/4.0(compatible; MSIE 5.5; Windows NT)'}
#
#r = requests.post('http://httpbin.org/post', json=payload, headers=headers)
# 发送到服务器请求的头部可以通过r.request.headers 访问；
#print r.request.headers
# 服务器返回给我们的响应头部信息可以通过r.headers 访问
#print r.headers

#当我们在使用requests.get/post/put 等等请求时，Requests做了两件事情：
#构建一个requests对象，给对象会根据请求方法和参数发起http请求
#一旦服务器响应，会产生一个response对象，该响应对象包含了服务器返回的所有信息；

# 例如可以访问响应对象的status_code属性；
#r = requests.get("http://httpbin.org/get")
#print r.status_code

#对于响应正文，可以通过多种方式读取：

# 可以使用r.text 来读取unicode形式的响应
#print r.text
#print r.encoding

# json 响应的内容，可以使用json()方法把返回的数据解析成python对象；
#r = requests.get("https://github.com/timeline.json")
#print r.headers.get('content-type')
#print r.json()

# 二进制响应，可以以字节的方式访问响应正文，访问content属性可以获取二进制数据；
# 比如用放回的二进制数据创建一张图片；

#url = 'https://github.com/reactjs/redux/blob/master/logo/logo.png?raw=true'
#r = requests.get(url)
#image_data = r.content   # 获取二进制数据
#
#with open('/Users/gongmike/desktop/redux.png', 'wb') as fout:
#    fout.write(image_data)

# 原始响应，在少数情况下，可能想获取来自父娶妻的原始套接字响应，可以通过访问响应对象的raw属性来实现



