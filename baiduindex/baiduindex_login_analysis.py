#encoding = utf-8

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import pytesseract

# 登陆百度的url
usernane = ''
password = ''
keyword = "金税三期"

browser = webdriver.Chrome()
url = "https://passport.baidu.com/v2/?login&tpl=mn&u=http%3A%2F%2Fwww.baidu.com%2F"
browser.get(url)
browser.maximize_window()
# 不知道为什么，那个窗口最大化的功能无法实现，这个问题还没有解决；
browser.find_element_by_id("TANGRAM__PSP_3__footerULoginBtn").click()
# 找到id，分别输入用户名和密码
namebox = browser.find_element_by_id("TANGRAM__PSP_3__userName")
namebox.send_keys(usernane)
passwordbox = browser.find_element_by_id("TANGRAM__PSP_3__password")
passwordbox.send_keys(password)
time.sleep(3)
# 睡眠三秒，点击回车登陆
loginbut = browser.find_element_by_id("TANGRAM__PSP_3__submit")
loginbut.send_keys(Keys.ENTER)
time.sleep(3)
# 这里百度有一个反爬虫措施，会让你输手机短信，其实这个叉掉，重新再登陆一次就行；唬人的把戏
close = browser.find_element_by_id("TANGRAM__22__header_a")
close.click()
time.sleep(3)
loginbut = browser.find_element_by_id("TANGRAM__PSP_3__submit")
loginbut.send_keys(Keys.ENTER)
browser.get('https://index.baidu.com')
# 
time.sleep(3)
input_word = browser.find_element_by_class_name("search-input")
input_word.send_keys("金税三期")
search_operate = browser.find_element_by_class_name('search-input-operate')
search_operate.click()








	













































	