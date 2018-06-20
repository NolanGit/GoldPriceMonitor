# coding=utf-8
import gold_price_getter as price_getter
from mail_sender import MailSender
import requests
import time
import itchat

receiver_addr = ['XXX@live.com', 'XXX@qq.com', 'XXX@outlook.com']  # 填写收件人邮箱
sender_name = 'GoldMonitor'
my_sender = 'XXX@qq.com'
my_pass = 'XXX'

# itchat.auto_login(hotReload=True)
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' 程序运行中...')
while 1:
    price = price_getter.get_price()
    if price < 265:  # 黄金价格一旦低于265.5
        subject = 'Goldprice'
        content = '黄金的价格目前为%s,价格较低，可以买入' % (price)
        MS = MailSender(my_sender, my_pass, sender_name, receiver_addr, subject, content)
        MS.send_it()
        time.sleep(7200)  # 两小时至多发一次
        # 微信发送消息至文件传输助手
#       itchat.send((time.strftime('%Y-%m-%d%H:%M:%S',time.localtime(time.time()))+Content),'filehelper')
        MailSender(SenderName, ReceiverAddr, Subject, Content)
    if price > 280:  # 黄金价格一旦高于275
        Subject = 'Goldprice'
        Content = '黄金的价格目前为%s,价格较高，可以卖出' % (price)
#       itchat.send((time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+Content),'filehelper')
        MS = MailSender(my_sender, my_pass, sender_name, receiver_addr, subject, content)
        MS.send_it()
        time.sleep(7200)  # 两小时至多发一次
    time.sleep(23)  # 每隔一定时间爬取一次黄金价格
print(('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '程序终止')
