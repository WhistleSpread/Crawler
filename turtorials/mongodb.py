#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 20:27:23 2018

@author: gongmike
"""

# shiyong python lianjie mongodb de yige ku pymongo
# pymongo 是python 的一个用来连接mongodb的一个库
# 首先需要安装mongodb，pymongo，

import pymongo
client = pymongo.MongoClient('localhost', 27017)
# 建立连接；现在mongodb的客户端就在python的程序中，我们操作client就是在操作mongodb；
# 因为我们建立的是本地连接，所有所用的参数是localhost和27017，如果是连接网络环境下的远程数据库，那么参数就是别的；

#接下来给数据库起一个名称：
galdor = client['galdor']
# 左边的这个是python中使用的对象；右边的那个是python中数据库的名称；这个数据库的名称叫做galdor；
#  一般建议这两个名称起的是一样的；这样方便操作；

# 在数据库database中创建collection，所以你现在操作的对象是database，也就是前面的galdor；
sheet_tab = galdor['sheet_tab']
# zuobian shi zai python duixaing zhong de mingcheng 
# youbian shi zai shujvkuzhong biaode mingcheng;
#
#jiexiaolai dakaiyige txt wenben ,ranhou ban duqude meiyihang,
#keishi jisuan meiiyihande dnaci ,jiugouhuan cunzai jiaozuo 
#sheet_lines de ye limina;

path=''
with open(path, 'r') as f:
    lines = f.readlines()
    for index, line in enumerate(lines):
        data = {
            'index':index,
            'line':line,
            'words':len(line.split())
            }
#        print data
#        将每一项data对象存到mongodb中；
        sheet_tab.insert_one(data)
        
for item in sheet_tab.find():
    # 需要表中的数据展现出来需要用到find方法；
    print item

    
# 如果要找到每条特定的数据项目，需要加上一个对象；也就是加上一个它拥有的键值对；

for item in sheet_tab.find({'words':0}):
    print item
    print item['line']


for item in sheet_tab.find({'words':{'$lt':5}}):
    # 筛选出所有的word字段值lesst than 5的数量的结果；
    #$lt, $gt, $lte, $gte, $ne e=equal
    print item
    print item['line']
    












































