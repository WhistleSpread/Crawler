# encoding = 'utf-8'
from baidu_login import *
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import pytesseract

# 思路：使用selenium中的ActionChains这个类，实现了模拟鼠标的移动。每次移动的距离就是从一天到下一天的距离。
# ActionChains(browser).move_to_element_with_offset(xoyelement, x_0, y_0).perform()

browser.maximize_window()
# 构造天数
rel = '//a[@rel="'+str(day)+'"]'
browser.find_element_by_xpath(rel).click()
# 找到图形框，也就是中间最大的曲线图形框；感觉这个css_selector的代码可以改进
# 这里通过css选择器选择，选择了id为trend下的第3个rect元素，也就是整个曲线框
xoyelement = browser.find_elements_by_css_selector("#trend rect")[2]
# 根据坐标点的不同可以构造偏移量
# 经过测试，如果选择是最近7天的话，那么两个cx的偏移量为 202.3333333 对于24h、30天、90天、半年、全部，可以测试cx的差值
# 用selenium库来模拟鼠标滑动悬浮：
from selenium.webdriver.common.action_chains import ActionChains
# ActionsChains的作用是自动化，自动化一些低层次的交互动作，比如说鼠标悬停，鼠标移动等等；
# 调用ActionChains声明一个动作链对象；
actions = ActionChains(browser)
# selenium 的 ActionsChains 对象提供一个move_to_element_with_offset(to_element, xoffset, yoffset) 方法
# Move the mouse by an offset of the specified element.
# Offsets are relative to the top-left corner of the element.
# to_element: The WebElement to move to.
actions.move_to_element_with_offset(xoyelement,x_0,y_0).perform()
x_0 = 1
y_0 = 0
# 根据api的说明，这里x_0和y_0 最开始点是左上角，所以一开始不会显示数字框，所以需要自己设置x_0和y_0

# 按照天数进行循环，让横坐标进行累加
for i in range(day):
	if day == 7:
	    x_0 = x_0 + 202.33
	elif day == 30:
		x_0 = x_0 + 41.68
	elif day == 90:
	    x_0 = x_0 + 13.64
	elif day == 180:
	    x_0 = x_0 + 6.78

# 当鼠标移动到相应的位置后，页面会弹框，我们可以用selenium 自动识别图框的位置
# 首先让那个浏览器找到这个对象；
img_box = browser.find_element_by_id("viewbox")
# 然后确定框中的大小和位置：
# 找到图片坐标
locations = img_box.location
# print(locations)
# 找到图片大小
sizes = img_box.size
# print(sizes)
# 构造每一个img_box的指数的位置，放在一个tuple中，分别是左上角的x和y，右下角的x和y
img_box_locations = (int(locations['x']), int(locations['y']), int(locations['x']+sizes['width']), int(locations['y']+sizes['height']),)
# 除此之外，在爬取全部数据信息的时候，针对这个img_box_locations 可以通过截图得到想要的数据；
# 现在想通过截图，只是得到包含的数据，只要数据，不要其他的东西，则可以通过暴力构造，得到新的index_num_locations
index_num_locations = (int(locations['x']+sizes['width']/3), int(locations['y']+sizes['height']/2), int(locations['x']+sizes['width']*2/3), int(locations['y']+sizes['height']))
# 这里左上角的坐标，x向移动宽度的1/3，y向下移动高度的1/2；
# 右下角的的坐标x是左上角坐标增加宽度的2/3，y是到底了；
# 确定好了要截取的坐标后，调用selenium的api，截图，作为图像识别的素材；
# 截取当前浏览器：
path = '../raw/baidu' + str(num)
# 保存屏幕截图
browser.save_screenshot(str(path) + ".png")
# 打开屏幕截图，根据index_num_locations，截取需要的指数数据图片

# 这个Image模块是图像处理库PIL的一个重要的模块，一般是用于图像处理；
# 打开截图，根据指数的位置截图；
screenshot = Image.open(str(path) + ".png")
index_num_pic = screenshot.crop(index_num_locations)
index_num_pic.save(str(path) + ".jpg")








































































