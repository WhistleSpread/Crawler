# encoding = 'utf-8'

from baidu_login import *
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import pytesseract
import os

path=os.getcwd()

def set_params(day, city=None, icon=None):
	"""
	这里是可调的参数,目前实现7、30、90、180
	之后会加入一些其他的可选参数，例如：地区、整体趋势、移动趋势等
	"""
	day = 30
	rel = '//a[@rel="'+str(day)+'"]'
	chartselect = browser.find_element_by_xpath('//a[@rel="'+str(day)+'"]')
	chartselect.click()
	return None

def mouse_move(x_0=1, y_0=4):
	"""
	模拟鼠标的移动
	"""
	xoyelement = browser.find_elements_by_css_selector("#trend rect")[2]
	actions = ActionChains(browser)
	actions.move_to_element_with_offset(xoyelement,x_0,y_0).perform()

def screen_shot():
	"""
	在模拟鼠标的移动之后，移动到特定的位置，会出现显示数字的小黑框，小黑框里就有我们想要的数据；
	数据在id为viewbox的div中出现，其display属性为none或者block；只有鼠标移上去才是block
	函数的作用是截取img_box,通过暴力构造index_num_locations，然后
	"""
	img_box = browser.find_element_by_id("viewbox")
	locations = img_box.location
	# print(locations)
	sizes = img_box.size
	# print(sizes)

	img_box_locations = (int(locations['x']), int(locations['y']), int(locations['x']+sizes['width']), int(locations['y']+sizes['height']),)
	date_locations = (int(locations['x']), int(locations['y']), int(locations['x']+sizes['width']), int(locations['y']+sizes['height']*1/2))
	index_num_locations = (int(locations['x']+sizes['width']/3), int(locations['y']+sizes['height']/2), int(locations['x']+sizes['width']*2/3), int(locations['y']+sizes['height']))
	
	path = '../raw_num_imgs/' + str(num)
	browser.save_screenshot(str(path) + ".png")
	screenshot = Image.open(str(img_path) + ".png")
	index_num_pic = screenshot.crop(index_num_locations)
	index_num_pic.save(str(path) + ".jpg")
	date_pic = screenshot.crop(date_locations)

	date_pic.save(str(path)+'.jpg')

def zoom_imgs(img_path):
	"""
	发现裁剪的图片太小，识别精度太低，所以需要对图片进行扩大
	这里将图片放大一倍 原图大小73.29
	这个函数写的有点问题，要修改一下；
	"""
	jpgzoom = Image.open(str(img_path) + ".jpg")
	(x, y) = jpgzoom.size
	x_s = 146
	y_s = 58
	zoomed_img = jpgzoom.resize((x_s, y_s), Image.ANTIALIAS)
	zoomed_img.save(path + 'zoom.jpg', 'png', quality=95)
	return zoomed_img_path


def trans_imgs_to_data(zoomed_img_path):
	"""
	利用图像识别包pytesseract对截取的图片进行图像识别
	将图片中的数字转化为字符串
	"""
	index_image = Image.open(str(path) + "zoom.jpg")
	num = pytesseract.image_to_string(index_image)
	if num:
		return num
		

def get_data(day, city, icon):
	set_params(day, city=None, icon=None)
	mouse_move()
	for i in range(day):
		if day == 7:
			x_0 = x_0 + 202.33
			mouse_move(x_0, y_0)
		elif day == 30:
			x_0 = x_0 + 41.68
			mouse_move(x_0, y_0)
		elif day == 90:
			x_0 = x_0 + 13.64
			mouse_move(x_0, y_0)
		elif day == 180:
			x_0 = x_0 + 6.78
			mouse_move(x_0, y_0)









