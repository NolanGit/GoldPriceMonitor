# coding=utf-8
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_time():
    CurrentHour = int(time.strftime('%H', time.localtime(time.time())))
    CurrentMin = int(time.strftime('%M', time.localtime(time.time())))
    CurrentTime = CurrentHour + CurrentMin / 100
    CurrentWeek = int(time.strftime('%w', time.localtime(time.time())))
    return CurrentTime, CurrentWeek


def get_price():
    while 1:
        try:
            CurrentTime, CurrentWeek = get_time()
            if CurrentWeek != 0 and CurrentWeek != 6:
                # if 8 < CurrentTime < 12 or 13.30 < CurrentTime < 16 or 20 < CurrentTime < 24:  # 仅在国内黄金市场开盘时间前后进行爬取，24点之后休息时间不爬
                if 8 < CurrentTime < 12 or 13.30 < CurrentTime < 20 or 20 < CurrentTime < 24:  # 仅在国内黄金市场开盘时间前后进行爬取，24点之后休息时间不爬
                    chrome_options = Options()
                    chrome_options.add_argument('--headless')
                    chrome_options.add_argument('--log-level=3')
                    driver = webdriver.Chrome(executable_path=(r'C:\\Program Files (x86)\\Google\Chrome\\Application\\chromedriver.exe'), chrome_options=chrome_options)
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
                                print(time.strftime('%Y-%m-%d %H:%M:%S',
                                                    time.localtime(time.time())) + 'logging error...')
                                with open('C:\\Users\\sunhaoran\\Documents\\goldLog.txt', 'a', encoding='UTF-8')as f:
                                    f.write(time.strftime('%Y-%m-%d %H:%M:%S',
                                                          time.localtime(time.time())))
                                    f.write(str(soup))
                                    f.write('=' * 50)
                                print(time.strftime('%Y-%m-%d %H:%M:%S',
                                                    time.localtime(time.time())) + 'logged...')
                                print(time.strftime('%Y-%m-%d %H:%M:%S',
                                                    time.localtime(time.time())) + '数据获取失败，三分钟后将重试')
                                time.sleep(180)
                            else:
                                break
                        else:
                            break
                    else:
                        break
                else:
                    print((time.strftime('%Y-%m-%d %H:%M:%S',
                                         time.localtime(time.time()))) + '当前非交易时间,5分钟后重试')
                    time.sleep(300)
            else:
                print((time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))) + '当前为星期%s非交易日，六小时后重试' % (CurrentWeek))
                time.sleep(21600)
        except Exception as e:
            print(e)
            continue
    price = divs.get_text()
    '''
    percent = ((float(price) - float(beginning_price)) / float(beginning_price)) * 100  # 265.74为购买价格
    print(time.strftime('%Y-%m-%d %H:%M:%S',
                        time.localtime(time.time())) + '数据获取成功:' + price + ',涨跌幅为' + str(round(percent, 3)) + '%' + '盈亏为' + str((round(percent, 3) * 75)))
    '''
    driver.quit()
    return float(price)
