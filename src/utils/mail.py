"""
    Author: kervias
    Content: send mail
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.header import Header


class QQMail:
    def __init__(self, data={}):
        self.data = data
        if 'type' not in data:
        	self.data['type'] = 'html' #可以为plain

    def send_email(self):
        message = MIMEMultipart()
        message['From'] = self.data['sender']
        message['To'] = ';'.join(self.data['receive'])
        message['Subject'] = Header(self.data['title'], 'utf-8').encode()

        message.attach(MIMEText(self.data['msg'], self.data['type'], 'utf-8'))  
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器
        server.login(self.data['sender'], self.data['password'])
        server.sendmail(self.data['sender'], self.data['receive'], message.as_string())
        server.quit()  # 关闭连接
