#coding=utf-8
import smtplib
import time
from email.mime.text import MIMEText
from email.utils import formataddr

class MailSender(object):

	def __init__(self,my_sender,my_pass,sender_name,receiver_addr,subject,content):
		self.my_sender=my_sender
		self.my_pass=my_pass#口令，不是密码，通常为16位字符串
		self.sender_name=sender_name
		self.receiver_addr=receiver_addr
		self.subject=subject
		self.content=content
		
	def send_it(self):
		msg=MIMEText(self.content,'plain','utf-8',)
		msg['From']=formataddr([self.sender_name,self.my_sender])
		msg['to']='管理员'  
		msg['Subject']=self.subject
		server=smtplib.SMTP_SSL("smtp.qq.com", 465)
		server.login(self.my_sender, self.my_pass)
		server.sendmail(self.my_sender,self.receiver_addr,msg.as_string())
		server.quit()
		print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'邮件发送成功')
