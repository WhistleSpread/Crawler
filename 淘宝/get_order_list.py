#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 16:39:09 2018

@author: gongmike
"""

import request
from bs4 import BeautifulSoup

class Taobao:
    
#    初始化方法
    def __init__(self):
        self.loginUrl = "https://login.taobao.com/member/login.jhtml"