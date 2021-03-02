"""
    Author: kervias
    Content: send mail
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.header import Header


class SMTPMail:
    smtp_dict = {
        '@qq.com': ('smtp.qq.com', 465),
        '@163.com': ('smtp.163.com', 465),
        '@gmail.com': ('smtp.gmail.com', 465)
    }

    def __init__(self, data=dict()):
        self.data = data
        self.smtp_i = self.smtp_port = None
        for k, v in self.smtp_dict.items():
            if data['sender'].endswith(k):
                self.smtp_ip = v[0]
                self.smtp_port = v[1]
                break
        if 'smtp_ip' in data.keys() and 'smtp_port' in data.keys():
            self.smtp_ip = data['smtp_ip']
            self.smtp_port = data['smtp_port']

        if self.smtp_ip is None:
            raise Exception("非法发件人邮箱名")

        if 'type' not in data:
            self.data['type'] = 'html'  # 可以为plain

    def send_email(self):
        message = MIMEMultipart()
        message['From'] = self.data['sender']
        message['To'] = ';'.join(self.data['receive'])
        message['Subject'] = Header(self.data['title'], 'utf-8').encode()

        message.attach(MIMEText(self.data['msg'], self.data['type'], 'utf-8'))
        server = smtplib.SMTP_SSL(self.smtp_ip, self.smtp_port)  # 发件人邮箱中的SMTP服务器
        server.login(self.data['sender'], self.data['password'])
        server.sendmail(self.data['sender'],
                        self.data['receive'], message.as_string())
        server.quit()  # 关闭连接
