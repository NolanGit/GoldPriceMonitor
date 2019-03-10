#coding=utf-8
import os
import sys
import time
import smtplib
import platform
import configparser
from email.utils import formataddr
from email.mime.text import MIMEText

cf = configparser.ConfigParser()
if 'Windows' in platform.platform() and 'Linux' not in platform.platform():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' Using C:/Users/sunhaoran/Documents/GitHub/ServerTools/ServerTools.config ...')
    cf.read('C:/Users/sunhaoran/Documents/GitHub/ServerTools/ServerTools.config')
elif 'Linux' in platform.platform() and 'Ubuntu' not in platform.platform():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' Using /home/pi/Documents/Github/ServerTools/ServerTools.config ...')
    cf.read('/home/pi/Documents/Github/ServerTools/ServerTools.config')
elif 'Ubuntu' in platform.platform():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' Using /root/Documents/GitHub/ServerTools/ServerTools.config ...')
    cf.read('/root/Documents/GitHub/ServerTools/ServerTools.config')
SENDER = cf.get('config', 'SENDER')
PASSWORD = cf.get('config', 'PASSWORD')
RECEIVER = cf.get('config', 'RECEIVER')


class MailSender(object):
    global SENDER
    global PASSWORD
    global RECEIVER

    def __init__(self, sender_name, subject, content, my_sender=SENDER, my_pass=PASSWORD, my_receiver=RECEIVER):
        self.my_sender = my_sender
        self.my_pass = my_pass  #口令，不是密码，通常为16位字符串
        self.sender_name = sender_name
        self.receiver_addr = my_receiver
        self.subject = subject
        self.content = content

    def send_it(self):
        msg = MIMEText(
            self.content,
            'plain',
            'utf-8',
        )
        msg['From'] = formataddr([self.sender_name, self.my_sender])
        msg['to'] = '管理员'
        msg['Subject'] = self.subject
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(self.my_sender, self.my_pass)
        server.sendmail(self.my_sender, self.receiver_addr, msg.as_string())
        server.quit()
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' 邮件发送成功')
