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
        #subject = self.data['title']  # 主体内容
        # subject = unicode(subject)# 更改主题编码
        message['Subject'] = Header(self.data['title'], 'utf-8').encode()

        message.attach(MIMEText(self.data['msg'], self.data['type'], 'utf-8'))  # 如果要发送html需要将plain改成html
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(self.data['sender'], self.data['password'])  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(self.data['sender'], self.data['receive'], message.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接


if __name__ == '__main__':
    data = {
        'receive': ['kervia1@qq.com'],
        'msg': "<h1>你好</h1>",
        'type': 'html'
    }
    mail = Mail(data)
    mail.send_email()