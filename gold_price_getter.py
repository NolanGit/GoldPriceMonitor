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


def get_gold_price():
    '''
    返回当前黄金价格
    '''

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--log-level=3')
    driver = webdriver.Chrome(executable_path=('/usr/lib/chromium-browser/chromedriver'), chrome_options=chrome_options)

    for x in range(5):
        driver.get("http://www.dyhjw.com/hjtd")
        time.sleep(5)
        current_html = driver.page_source
        soup = BeautifulSoup(current_html, 'lxml')

        divs = soup.find(class_='nom last green')
        if not divs:
            divs = soup.find(class_='nom last red')
            if not divs:
                divs = soup.find(class_='nom last ')
                if not divs:
                    print('=' * 20 + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))) + '=' * 20)
                    print(str(soup))
                    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '数据获取失败，三分钟后将重试')
                    time.sleep(180)
                else:
                    break
            else:
                break
        else:
            break

    if divs:
        return float(divs.get_text())
    else:
        return None
    driver.quit()


a = get_app_price()
print(a)