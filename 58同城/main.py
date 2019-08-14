from multiprocessing import Pool
# 这个库可以让python 调用电脑主机cpu的多个内核来完成任务；
from channel_extract import channel_list
from page_pare import get_links_from

def get_all_links_from(channel):
	for num in range(1, 101):
		get_links_from(channel, num)

# pool = Pool()
# 创建一个进程池，所有的爬虫，都会被扔到池子当中；然后分配个所有的进程，让他进行一个多进程的处理；
# 所有的cpu，所有的程序（在这里就是我们写的爬虫函数），都要从进程池中取它被分配的任务；
# 实际上，这个进程池有一个参数process，pool = Pool(processes=4)这个参数告诉你，要开多少个进程；进程数越多给cpu的负担就越大；
#  建议自动分配，也就是空着；他会分析你有多少个内核；

# pool.map(get_all_links_from, channel_list.split())
# channel_list.split()是从所有的频道列表中得到链接，这个返回的是一个list，这个list中是所有的频道链接；



# 如果爬虫跑到一半的时候停了？如何从停了的位置重新来启动爬虫呢？
#  可以使用set这种数据结构；set和list的行为类似，区别在于，set不能包含重复的值。
#  set的操作有交集和差集；

#  下面这两个都是列表解析式，也称为列表推倒式，推导式可以从一个数据序列构建出另一个新的数据序列结构体
#  对于list\dict\set\都行；

# db_urls = [item['url'] for item in url_list.find()]
#  db_urls 返回的是一个list，这个list中每个元素都是数据库中的一个item元素的url；
# index_urls = [item['url'] for item in item_info.find()]
# index_urls 返回的是一个list，这个list是所有的item_info 这个collection中国
# x = set(db_urls)
#  整理是将db_urls 变成了一个set，这个set具有不可重复性的特性；这个set包含的是所有的
# y = set(index_urls)
#  同理，将index_urls 变成了一个set
# rest_of_urls = x-y
#  set具有差集操作运算，因为x集合相当于是所有的二手商品的集合，而y是抓取下来的详情页的集合
#  两个做差，就得到了还没有抓取到的，剩余的二手商品的详情页；
#  下次重新开始抓取的时候就不需要从db_url 中抓取了， 只需要从rest_of_urls 中抓取即可；

if __name__ == '__main__':
	print('开始了！')
	pool = Pool()
	pool.map(get_all_links_from, channel_list.split())




	

