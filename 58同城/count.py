#  这个是一个小的监控程序；用来计数；
#  每隔5秒钟就查看一下url_list这个collection，看看爬取了多少数据；
#  这里的url_list 就是一个二手商品的详情页的信息；

import time
from page_pare import url_list


while True:
	print(url_list.find().count())
	# find() 方法可以查询集合中的所有数据
	# count()统计数据的数量；
	time.sleep(5)