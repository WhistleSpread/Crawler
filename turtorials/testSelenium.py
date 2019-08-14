#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 17:08:50 2018

@author: gongmike
"""

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Chrome()

browser.get('https://login.taobao.com/member/login.jhtml')
wait = WebDriverWait(browser, 10)

static2Quick = browser.find_element_by_id("J_Quick2Static")

ActionChains(browser).click(static2Quick).perform()
# perform()函数不要忘记了，只有在perform()加入之后才会执行；

username = browser.find_element_by_id('TPL_username_1')
ActionChains(browser).click(username).perform()
username.send_keys('xxxxxx')
password = browser.find_element_by_id('TPL_password_2')
ActionChains(browser).click(password).perform()
password.send_keys('xxxxxx')
button = browser.find_element_by_id('J_SubmitStatic')
ActionChains(browser).click(button).perform()

WebMonPwd

