# -*- coding:utf-8 -*-
import os
import sys
import time
import peewee
import datetime
import requests
import platform
import configparser
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.path.append('../')
sys.path.append('../../')
from Common.Tools import Tools
from Common.model import Price
from Common.Mail_Sender import MailSender
from Common.Global_Var import Global_Var


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
    driver.quit()
    if divs:
        return float(divs.get_text())
    else:
        return None


def save_data(price):
    try:
        crawling_times = int(len(Price.select().where(Price.date == datetime.datetime.now().date())))
    except Exception:
        crawling_times = 0
    p = Price(price=price, date=datetime.datetime.now().date(), crawling_times=crawling_times, time=datetime.datetime.now().strftime('%H:%M:%S'))
    p.save()
    print('price saved...')


def send_mail_threshold(max, min, price):
    cf = configparser.ConfigParser()
    if 'Windows' in platform.platform() and 'Linux' not in platform.platform():
        cf.read('C:/Users/sunhaoran/Documents/GitHub/ServerTools/ServerTools.config')
    elif 'Linux' in platform.platform() and 'Ubuntu' not in platform.platform():
        cf.read('/home/pi/Documents/Github/RaspberryPi.config')
    elif 'Ubuntu' in platform.platform():
        cf.read('/root/Documents/GitHub/ServerTools/ServerTools.config')
    GOLD_MAIL_FLAG = cf.get('config', 'GOLD_MAIL_FLAG')

    price = int(price)
    if (price > max or price < min) and GOLD_MAIL_FLAG:
        mail = MailSender('Administrator', 'Gold Price Monitor', 'current gold price is ' + price)


price = get_gold_price()
save_data(price)
send_mail_threshold(300, 270, price)
