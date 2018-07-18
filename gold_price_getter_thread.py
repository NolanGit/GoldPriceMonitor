# coding=utf-8
import time
import queue
import threading
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_time():
    CurrentHour = int(time.strftime('%H', time.localtime(time.time())))
    CurrentMin = int(time.strftime('%M', time.localtime(time.time())))
    CurrentTime = CurrentHour + CurrentMin / 100
    CurrentWeek = int(time.strftime('%w', time.localtime(time.time())))
    return CurrentTime, CurrentWeek


week_flag = 1
hour_flag = 1
work_flag = 1
hour_flag_changer_flag = 0
week_flag_changer_flag = 0
work_flag_change_flag = 0
q = queue.Queue()
lock = threading.Lock()


def get_price():
    global week_flag
    global hour_flag
    global hour_flag_changer_flag
    global week_flag_changer_flag
    CurrentTime, CurrentWeek = get_time()
    if CurrentWeek != 0 and CurrentWeek != 6 and week_flag == 1:
        if (8 < CurrentTime < 12 or 13.30 < CurrentTime < 16 or 20 < CurrentTime < 24) and hour_flag == 1:
            start_get_price_thread = threading.Thread(target=start_get_price)
            start_get_price_thread.start()
            start_get_price_thread.join()
            result = list()
            result.append(q.get())
            return result[0]
        else:
            lock.acquire()
            hour_flag = 0
            lock.release()
            if hour_flag_changer_flag == 0:  # 如果hour_flag没有正在被更改中
                threading.Thread(target=hour_flag_changer).start()
            else:
                pass
    else:
        lock.acquire()
        week_flag = 0
        lock.release()
        if week_flag_changer_flag == 0:  # 如果week_flag没有正在被更改中
            threading.Thread(target=week_flag_changer).start()
        else:
            pass


def hour_flag_changer():
    global week_flag
    global hour_flag
    lock.acquire()
    hour_flag_changer_flag = 1  # 加锁
    lock.release()
    threading.Timer(300, change_hour_flag).start()
    q.put(('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '当前非交易时间,五分钟后重试')


def change_hour_flag():
    global week_flag
    global hour_flag
    lock.acquire()
    hour_flag = 1
    lock.release()
    lock.acquire()
    hour_flag_changer_flag = 0  # 释放锁
    lock.release()


def week_flag_changer():
    global week_flag
    global hour_flag
    lock.acquire()
    week_flag_changer_flag = 1  # 加锁
    lock.release()
    threading.Timer(21600, change_week_flag).start()
    q.put(('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '当前为星期%s非交易日，六小时后重试' % CurrentWeek)


def change_week_flag():
    global week_flag
    global hour_flag
    lock.acquire()
    week_flag = 1
    lock.release()
    lock.acquire()
    week_flag_changer_flag = 0  # 释放锁
    lock.release()


def start_get_price():
    global work_flag
    if work_flag == 1:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--log-level=3')
        driver = webdriver.Chrome(executable_path=(r'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe'), chrome_options=chrome_options)
        driver.get("http://www.dyhjw.com/hjtd")
        time.sleep(5)
        current_html = driver.page_source
        soup = BeautifulSoup(current_html, 'lxml')
        divs = soup.find(class_='nom last green')
        if divs == None:
            divs = soup.find(class_='nom last red')
            if divs == None:
                divs = soup.find(class_='nom last ')
                if divs == None:
                    lock.acquire()
                    work_flag = 0
                    lock.release()
                    if work_flag_change_flag == 0:
                        threading.Thread(target=work_flag_changer).start()
                    else:
                        pass
                else:
                    price = divs.get_text()
                    driver.quit()
                    q.put(price)
            else:
                price = divs.get_text()
                driver.quit()
                q.put(price)
        else:
            price = divs.get_text()
            driver.quit()
            q.put(price)
    else:
        pass


def work_flag_changer():
    lock.acquire()
    work_flag_change_flag = 1
    lock.release()
    threading.Timer(180, change_work_flag).start()
    q.put(('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '数据获取失败，三分钟后将重试')


def change_work_flag():
    global work_flag
    lock.acquire()
    work_flag = 1
    lock.release()
    lock.acquire()
    work_flag_change_flag = 0
    lock.release()


'''
	                    print(time.strftime('%Y-%m-%d %H:%M:%S',
	                                        time.localtime(time.time())) + 'logging error...')
	                    with open('C:\\Users\\sunhaoran\\Documents\\goldLog.txt', 'a', encoding='UTF-8')as f:
	                        f.write(time.strftime('%Y-%m-%d %H:%M:%S',
	                                              time.localtime(time.time())))
	                        f.write(str(soup))
	                        f.write('=' * 50)
	                    print(time.strftime('%Y-%m-%d %H:%M:%S',
	                                        time.localtime(time.time())) + 'logged...')
	                    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '数据获取失败，三分钟后将重试')
'''
