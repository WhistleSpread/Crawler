#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# 注意，selenium 在这个电脑的python2 是没有安装的，只在python3中安装了；
# 在终端中运行代码即可；

# 小例子，利用selenium 驱动chrome 完成的操作； 
# 输入问题
# 敲回车
# 等待加载
# 获取源代码



# 基本使用
from selenium import webdriver
#这个webdriver 实际上就是浏览器信息的对象；
from selenium.webdriver.common.by import By
# 利用By类来确定哪种选择方式
from selenium.webdriver.common.keys import Keys
# 利用Key类来模拟键盘的输入操作
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Chrome()
# 声明了一个浏览器对象；

try:
   browser.get('https://www.baidu.com')
   # 调用这个对象的get方法，传入url，然后它就会给你跳出一个浏览器，然后访问百度这个网址；
   input = browser.find_element_by_id('kw')
   # 用find_element_by_id()这个方法，找到了id为kw的元素，将其赋值为input；
   input.send_keys('Python')
   # 调用send_keys方法，模拟在浏览器输入框中键入“python”
   input.send_keys(Keys.ENTER)
   # 调用send_keys方法，模拟敲入回车；
   wait = WebDriverWait(browser, 10)
   # 调用等待，等待id为content_left的元素被加载出来；
   wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
   # 这里好奇怪啊，((By.ID, 'content_left'))，这里要加2层括号才运行的出来；要不然就运行不出来；
   # 因为参数是元组类型；
   # 等待id为‘content_left’的元素被加载出来；
   print(browser.current_url)
   # 打印出当前的url，百度搜索的链接；
   # 说不定可以根据这个来获得页面里没有规律的url；
   print(browser.get_cookies())
   # 打印cookies，列表
   print(browser.page_source)
   # 打印页面的源代码
   # 得到了源代码，就可以对源代码进行解析，然后就可以提取返回的结果了；
finally:
   browser.close()
   # 用try finally 把代码包围起来，最后把浏览器关掉；

# 声明浏览器对象：
# 首先映入webdriver库
from selenium import webdriver

# 生成一个浏览器对象，然后利用这个浏览器对象进行各种浏览器的操作；
# 可以查看官方文档，看一下支持的浏览器有哪些
browser = webdriver.Chrome()
browser = webdriver.Firefox()
browser = webdriver.Edge()
browser = webdriver.PhantomJS() 
browser = webdriver.Safari()    


# 访问页面
from selenium import webdriver
browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
# 利用browser对象的get方法，传入网址后，打开这个网址，访问这个网址；
print(browser.page_source)
# page_source 方法，获得网页的源代码，并打印出来；
browser.close()

# 查找元素
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
# 现在得到了一个网页，之后可能需要对这个网页进行交互的操作；
# 比如说，找到一个输入框，输入一些信息，找到一些按钮，然后点击这个按钮；
# 下面都是如何来获取一个元素；

# 用id来寻找一个元素，
input_first = browser.find_element_by_id('q')
# 用css选择器来选择元素；
input_second = browser.find_element_by_css_selector('#q')
# 用xpath 这种方法来选择，其实这三个做的是一样的事情；
input_third = browser.find_element_by_xpath('//*[@id="q"]')
print(input_first, input_second, input_third)
browser.close()

# 常用的选取单个元素的方法方法：
find_element_by_name
find_element_by_xpath
find_element_by_link_text
find_element_by_partial_link_text
find_element_by_tag_name
find_element_by_class_name
find_element_by_css_selector




# 另外，一个通用的查找方式：直接调用 find_element, 这个方法的第一个参数是By.XX,第二个参数是要查找的对象；
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
# 这种方法，相当于是上面的那种方法的一种通用的写法，这方法可以改写成上面的所有的方法
# ID = "id"
# XPATH = "xpath"
# LINK_TEXT = "link text"
# PARTIAL_LINK_TEXT = "partial link text"
# NAME = "name"
# TAG_NAME = "tag name"
# CLASS_NAME = "class name"
# CSS_SELECTOR = "css selector"

input_first = browser.find_element(By.ID, 'q')
input_second = browser.find_element(By.CSS_SELECTOR, '#q')
input_third = browser.find_element(By.XPATH, '//*[@id="q"]')
# 这三句话所做的事情其实是同一件事情
print(input_first)
browser.close()

# 查找多个元素； 注意，这里是find_elements 末尾加了s
# 常用的选取多个元素的方法：
find_elements_by_name
find_elements_by_xpath
find_elements_by_link_text
find_elements_by_partial_link_text
find_elements_by_tag_name
find_elements_by_class_name
find_elements_by_css_selector

from selenium import webdriver
browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
lis = browser.find_elements_by_css_selector('.service-bd li')
print(lis)
browser.close()
# 因为是多个元素，最后会以list的形式呈现；要获取其中的单个元素，用索引即可；

# 类似的，在查找多个元素时，可存在一种通用的方法：
from selenium import webdriver
from selenium.webdriver.common.by import By
browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
lis = browser.find_elements(By.CSS_SELECTOR, '.service-bd li')

#元素交互操作
# 对获得的元素调用交互方法；
# 在获取了元素引用之后，如何对获取后的元素进行操作呢？
# 比如，在获得了一个文本框之后，要在这个文本框中输入一行文字；然后对按钮，调用一个点击；
# 最简单的 sendkeys；click等方法；

from selenium import webdriver
import time
browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
# 因为在网页中，每个元素的id是唯一的，所以这里用id，不会出现重复；
input = browser.find_element_by_id('q')
input.send_keys('iPhone')
# 等了1s之后，将文本框清空；
time.sleep(1)
input.clear()
input.send_keys('iPad')
# 通过class_name 获得button；
button = browser.find_element_by_class_name('btn-search')
button.click()

# 可以通过webdriver的api，其中的WebDriver来操作；
# 交互动作，将动作附加到动作链中串行执行；
# 驱动浏览器为我们执行相关的交互；这个和元素交互不同，
# 需要引入ActionChains，可以模拟一个拖拽的动作；
from selenium import webdriver
from selenium.webdriver import ActionChains

browser = webdriver.Chrome()
url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
# 最开始是请求了一个url
browser.get(url)
# 切换到了iframeReuslt，frame是html的一个比较常用的标签；这句话就是切换到里面的iframe
browser.switch_to.frame('iframeResult')
# 切换到了iframe里面之后，找到被拖拽的对象source，以及要拖拽的目标target
source = browser.find_element_by_css_selector('#draggable')
target = browser.find_element_by_css_selector('#droppable')
# 调用ActionChainst声明一个动作链对象；
actions = ActionChains(browser)
# 调用动作链的方法drag_and_drop，这样把soruce 拖拽到target上面；
actions.drag_and_drop(source, target)
# 执行动作；
actions.perform()      
# 更加详细的见api 例如click double-click 等等；                                          

# 用Selenium直接运行js命令；
# 在元素交互的动作的时候，有些动作在Selenium中没有提供api，比如说：想要实现进度条下拉；
# 那么，我们可以通过执行JavaScript来实现进度条的拖拽；
# 因为Selenium提供了一个excute_script()这个api，你可以传入一些js语句
# 在元素交互动作比较难实现的时候，也可以使用javascript，这个api相当于是一个万能的方法了；
# 可以让浏览器动态的执行js想要实现的动作；

from selenium import webdriver
browser = webdriver.Chrome()
browser.get('https://www.zhihu.com/explore')
browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
browser.execute_script('alert("To Bottom")')


# 如何获取元素的信息
# 例如，我们已经用find_element_by_id获取了元素，那么如何获取这元素的属性？
# 获取知乎logo的信息，然后打印属性；
from selenium import webdriver
from selenium.webdriver import ActionChains

browser = webdriver.Chrome()
url = 'https://www.zhihu.com/explore'
browser.get(url)
logo = browser.find_element_by_id('zh-top-link-logo')
# 这个logo其实是一个对象；
print(logo)
print(logo.get_attribute('class'))

# 获取文本值
from selenium import webdriver

browser = webdriver.Chrome()
url = 'https://www.zhihu.com/explore'
browser.get(url)
input = browser.find_element_by_class_name('zu-top-add-question')
print(input.text) # 这个是获取这里写的文本

# 获取id、位置、标签名称、大小
from selenium import webdriver
browser = webdriver.Chrome()
url = 'https://www.zhihu.com/explore'
browser.get(url)
input = browser.find_element_by_class_name('zu-top-add-question')
print(input.id)
print(input.location) # 在浏览器中的位置
print(input.tag_name) # 标签名是个button；
print(input.size) # 在浏览器中占多少像素；高度，宽度；


# Frame的相关操作
# frame在网页中出现比较频繁，出现了frame，在元素筛选时，可能会导致不太方便的问题；
# frame相当于是独立的框架，在父级的frame里想要查找子元素的frame，需要切换到frame里查找才可以；
# 否则无法完成元素的查找；下例显示了如何切换到子元素的frame；
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

browser = webdriver.Chrome()
url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
browser.get(url)
# 传入的是这个frame的id，然后就会切换到这个frame
browser.switch_to.frame('iframeResult')
# 切换到了iframe里面之后，找到被拖拽的对象source，以及要拖拽的目标target
source = browser.find_element_by_css_selector('#draggable')
print(source)
try:
   logo = browser.find_element_by_class_name('logo')
   # 因为这个class name 为logo的对象在frame外面，所以会报错；
except NoSuchElementException:
   print('NO LOGO')
browser.switch_to.parent_frame()
logo = browser.find_element_by_class_name('logo')
print(logo)
print(logo.text)



# 元素等待的相关操作：
# 在做爬取的时候，可能有一些ajax请求，这些ajax请求，不会管selenium又没有完成网页的加载
# selenium只是把基本的框架加载出来了，如果有后续的ajax请求，可能有些元素没有加载完全，这样在进行
# 操作的时候会导致问题；在这里需要加一个等待，延长时间，确保元素都已经加载完成之后然后再进行操作；这样可以减少异常；

# 等待分为 隐式等待和显式等待；
#隐式等待：到了一定的时候，发现这个元素还没有加载出来，那么就继续等待，等待到你指定的时间
# 如果超出了你指定等待的时间，还是找不到这个元素，那么就会抛出异常；
# 如果在你指定的时间内找到了这个元素，那么它就会立即返回；隐式等待默认时间为0

# 当时用隐式等待执行测试的时候，如果WebDriver没有在Dom中找到元素，将继续等待，超出设定
#时间后，则抛出找不到元素的异常，换句话说，当查找元素或元素并没立即出现时，隐式等待将
#等待一段时间再查找Dom，默认时间为0

# 一般隐式等待使用的场景是在你的网速非常满的情况下，加载不出来，然后加一个等待时间；确保正常加载

from selenium import webdriver
browser = webdriver.Chrome()
browser.implicityly_wait(10)
# 传入你设置的隐式等待的时间；
browser.get('https://www.zhihu.com/explore')
input = browser.find_element_by_class_name('zu-top-add-question')
print(input)

# 显式等待；
# 你指定一个等待条件和一个最长等待时间，它会在这个最长等待时间内判断这个等待条件是否成立；
# 如果成立，会立即返回，如果不成立，则会一直等待，直到等待到最长的等待时间，如果还是不满足条件
# 则抛出异常；如果在等待时间内满足条件，则正常返回；
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
browser.get('http://www.taobao.com/')
# 声明一个WebDriverWait对象，将browser作为参数传入，并传入最长等待时间；并把对象赋给wait；
wait = WebDriverWait(browser, 10)
# 使用wait.until 这个方法，传入的是等待的条件，等待条件的参数是元组类型；
# 通过它可以指定一个显示等待的条件，如果获取到了这个元素，就会将这个元素赋值给input；
# 如果没有获取到这个元素，则抛出异常；
input = wait.until(EC.presence_of_element_located((By.ID, 'q')))
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-search')))
print(input, button)

# 如下是在显式等待的一些判断条件；更加详细的的api见excepted conditions support
# title_is 标题是某内容
# title_contains 标题包含某内容
# presence_of_element_located 元素加载出，传入定位元组，例如(By.ID, 'q')
# visibility_of_element_located 元素可见，传入定位元组
# visibility_of 可见，传入元素对象
# presence_of_all_elements_located 所有元素加载出
# text_to_be_present_in_element 某个元素文本包含某文字
# text_to_be_present_in_element_value 某个元素值包含某文字
# frame_to_be_avaliable_and_switch_to_it frame加载并切换
# invisible_of_element_located 元素不可见
# element_to_be_clickable 元素可点击



# 浏览器的前进和后退
import time
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.baidu.com/')
browser.get('https://www.taobao.com/')
browser.get('https://www.python.org/')
browser.back()
time.sleep(1)
browser.forward()
browser.close()


# cookies 在爬取的时候是非常有用的，尤其是在一些登陆之后的爬取，
# 可以用cookies设置登陆的状态等待；
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.zhihu.com/explore')
print(browser.get_cookies())
browser.add_cookie({'name':'name', 'domain':'www.zhihu.com', 'value':'germey'})
print(browser.get_cookies())
browser.delete_all_cookies()
print(browser.get_cookies())

# 使用webdriver 可以更改User-Agent
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('user-agent="Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"')
driver = webdriver.Chrome(chrome_options=options)
driver.get('https://www.baidu.com/')


# 选项卡管理：
# 可以通过执行一句js来打开网页的选项卡；
# 或者通过模拟快捷键来打开一个新的选项卡；
# 最好的方法是执行js，执行window.open()

import time
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.baidu.com')
browser.execute_script('window.open()')
print(browser.window_handles) 
# 返回所有选项卡
browser.switch_to.window(browser.window_handles[1])
browser.get('https://www.taobao.com')
time.sleep(1)
browser.switch_to.window(browser.window_handles[0])
browser.get('https://python.org')




# 异常处理
from selenium import webdriver
from selenium.common.exceptions import TimeOutException, NoSuchElementException

browser = webdriver.Chrome()
try:
   browser.get('http://www.baidu.com')
except TimeOutException:
   print('Time Out')
finally:
   browser.close()











































    
    