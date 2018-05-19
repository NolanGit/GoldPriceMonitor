#coding=utf-8
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import time
import itchat

def GetPrice():
	while 1:
		baseurl='http://www.dyhjw.com/hjtd'
		r = requests.get(baseurl)
		time.sleep(5)#避免网速低而加载过慢
		content=r.text
		soup = BeautifulSoup(content, 'lxml') 
		divs=soup.find(class_='nom last green')
		if divs==None:
			divs=soup.find(class_='nom last red')
			if divs==None:
				print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'logging error...')
				with open('C:\\Users\\sunhaoran\\Documents\\goldLog.txt','a',encoding='UTF-8')as f:
					f.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
					f.write(str(soup))
					f.write('============================================================')
				print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'logged...')
				print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'数据获取失败，五分钟后将重试')
				time.sleep(300)
			else:
				break
		else:
			break
	price=divs.get_text()
	print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'数据获取成功:'+price)
	return float(price)
def MailSender(SenderName,ReceiverAddr,Subject,Content):
	my_sender='XXXXX@qq.com'
	my_pass = 'XXXXX'#这个是需要到QQ邮箱里边获取的口令，不是QQ邮箱密码
	ReceiverName='Receiver'
	msg=MIMEText(Content,'plain','utf-8',)
	msg['From']=formataddr([SenderName,my_sender])
	msg['To']=formataddr(ReceiverAddr)
	msg['Subject']=Subject
	server=smtplib.SMTP_SSL("smtp.qq.com", 465)
	server.login(my_sender, my_pass)
	server.sendmail(my_sender,ReceiverAddr,msg.as_string())
	server.quit()
	print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'邮件发送成功，一小时后重新获取...')
	time.sleep(7200)#每小时至多发送一次邮件
def GetTime():
	CurrentHour=int(time.strftime('%H',time.localtime(time.time())))
	CurrentMin=int(time.strftime('%M',time.localtime(time.time())))
	CurrentTime=CurrentHour+CurrentMin/100
	return CurrentTime


itchat.auto_login(hotReload=True)
print('程序运行中...')
ReceiverAddr=['XXX@live.com','XXX@qq.com']#填写收件人邮箱
SenderName='GoldMonitor'
while 1:
	CurrentTime,CurrentWeek=GetTime()
	if CurrentWeek!=0 and CurrentWeek!=6:
		while 8<CurrentTime<12 or 13.30<CurrentTime<16 or 20<CurrentTime<24:#仅在国内黄金市场开盘时间前后进行爬取，24点之后休息时间不爬
			price=GetPrice()
			if price<265.5:#黄金价格一旦低于265.5
				Subject='Goldprice'
				Content='黄金的价格目前为%s,价格较低，可以买入'%(price)
				itchat.send((time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+Content),'filehelper')#微信发送消息至文件传输助手
				MailSender(SenderName,ReceiverAddr,Subject,Content)
			if price>280:#黄金价格一旦高于275
				Subject='Goldprice'
				Content='黄金的价格目前为%s,价格较高，可以卖出'%(price)
				itchat.send((time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+Content),'filehelper')
				MailSender(SenderName,ReceiverAddr,Subject,Content)
			time.sleep(10)#每十秒爬取一次黄金价格
		print((time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+'当前非交易时间,5分钟后重试'+CurrentTime)
		time.sleep(300)
	else:
		print((time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+'当前为星期%s非交易日，六小时后重试'%(CurrentWeek))
		time.sleep(21600)
print('程序终止')
