#coding=utf-8
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import time

def GetPrice():
	while 1:
		baseurl='http://www.dyhjw.com/hjtd'
		r = requests.get(baseurl)
		content=r.text
		soup = BeautifulSoup(content, 'lxml') 
		divs=soup.find(class_='nom last green')
		if divs==None:
			divs=soup.find(class_='nom last red')
			if divs==None:
				print('数据获取失败，五分钟后将重试')
				time.sleep(300)
			else:
				break
		else:
			break
	price=divs.get_text()
	return float(price)
def Mail(price):
	my_sender='XXX@qq.com'
	my_pass = 'XXX'#这个是需要到QQ邮箱里边获取的口令，不是QQ邮箱密码
	my_user='XXXX@XX.XX;XXXX@XX.XX'
	msg=MIMEText('黄金的价格目前为%s'%(price),'plain','utf-8',)
	msg['From']=formataddr(["GoldMonitor",my_sender])
	msg['To']=formataddr(["XXXX@XX.XX",my_user])
	msg['Subject']="GoldPrice"
	server=smtplib.SMTP_SSL("smtp.qq.com", 465)
	server.login(my_sender, my_pass)
	server.sendmail(my_sender,[my_user,],msg.as_string())
	print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'邮件发送成功，一小时后重新获取')
	server.quit()
	time.sleep(3600)#每小时至多发送一次邮件
def GetTime():
	CurrentHour=int(time.strftime('%H',time.localtime(time.time())))
	CurrentMin=int(time.strftime('%M',time.localtime(time.time())))
	CurrentTime=CurrentHour+CurrentMin/100
	return CurrentTime
	
print('程序运行中...')
CurrentTime=GetTime()
while 8<CurrentTime<12 or 13.30<CurrentTime<16 or 20<CurrentTime<24::#仅在国内黄金市场开盘时间前后进行爬取，24点之后休息时间不爬
	price=GetPrice()
	if price<266:#黄金价格一旦低于266
		Mail(str(price))
	time.sleep(10)#每十秒爬取一次黄金价格
print('程序终止')