# -*- coding:utf-8 -*-
import re
import sys
import time
import queue
import requests
import threading
sys.path.append('../')
sys.path.append('../../')
from bs4 import BeautifulSoup
from selenium import webdriver
from Common.Tools import Tools
#from Common.Mail_Sender import MailSender
from Common.Global_Var import Global_Var
from selenium.webdriver.chrome.options import Options
q = queue.Queue()


def get_app_price():
    '''
        爬取数据：接收app的Url后缀，返回app的名字和价格。
    '''
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--log-level=3')
    driver = webdriver.Chrome(executable_path=('/usr/lib/chromium-browser/chromedriver'), chrome_options=chrome_options)
    driver.get("http://www.dyhjw.com/hjtd")
    time.sleep(5)
    current_html = driver.page_source
    print (current_html)
get_app_price()