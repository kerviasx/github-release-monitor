from utils.template import TEMPLATE
from utils.mail import QQMail


import requests
from bs4 import BeautifulSoup
import queue
import threading
import logging
import json


class GithubReleaseSpider(object):
    def __init__(self, conf):
        self.conf = conf
        self.init_sipder_params()
        self.init_history_info()
        self.queue = queue.Queue()

    def init_sipder_params(self):
        self.headers = {
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'text/html; charset=UTF-8',
            'accept': 'text/html',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }
        

    def init_history_info(self):
        self.history_info = json.load(open(self.conf.DATA_FILE_PATH, 'r', encoding='utf8'))

    def get_monitor_urls(self):
        ret_list = []
        for name, value in self.conf.GITHUB_RELEASES.items():
            ret_list.append([name, value])
        return ret_list

    def spider(self, item):
        th_id = threading.currentThread().ident
        name,url = item[0],item[1]
        logging.info("[ID={}]:{}->{}".format(th_id, item[0], item[1]))
        result = None
        try:
            s = requests.session()
            s.headers.update(self.headers)
            s.keep_alive = False
            resp = s.get(url, verify=False)
            s.close()
            soup = BeautifulSoup(resp.text, 'html.parser')
            soup = soup.select('.release-entry')
            for item in soup:
                temp = item.select('.flex-self-start')
                label = temp[0].text.strip() if len(temp) > 0 else "空"
                temp = item.select('.css-truncate-target')
                tag = temp[0].text.strip() if len(temp) > 0 else "空"
                temp = item.select('.release-header a')
                title = temp[0].text.strip() if len(temp) > 0 else "空"
                temp = item.select('.markdown-body')
                # .text.strip().replace('\n','<br/>')
                content = str(temp[0]) if len(temp) > 0 else "空"
                result = {
                    'label': label,
                    'tag': tag,
                    'title': title,
                    'content': content,
                    'url': url
                }
                break
        except Exception as e:
            logging.error("[ID={}]:{}".format(th_id, str(e)))
            if name in self.history_info:
                result = self.history_info[name]

        self.queue.put([name, result])

    def parse_que_data(self):
        size = self.queue.qsize()
        temp = [self.queue.get() for i in range(size)]
        self.new_info = {}
        for i in temp:
            self.new_info[i[0]] = i[1]

    def save_result(self):
        self.parse_que_data()

        new_dict_info = self.new_info
        old_dict_info = self.history_info

        update_dict_info = {}
        # 遍历新的字典信息，找出与旧信息不同点
        for name, item in new_dict_info.items():
            if item == None:
                result = {
                    'label': "null",
                    'tag': "null",
                    'title': name,
                    'content': "null",
                    'url': self.conf.GITHUB_RELEASES[name]
                }
            if name not in old_dict_info.keys():
                update_dict_info[name] = item
            else:
                if new_dict_info[name]['label'] != old_dict_info[name]['label'] or new_dict_info[name]['tag'] != old_dict_info[name]['tag']:
                    update_dict_info[name] = item

        # write to the file
        with open(self.conf.DATA_FILE_PATH, 'w', encoding='utf8') as f:
            json.dump(new_dict_info, f, indent=4, ensure_ascii=False)

        self.send_email(update_dict_info)

    
    def send_email(self, update_dict_info):
        #print(update_dict_info)
        if update_dict_info.__len__() == 0:
            logging.info("所有项目均未发布新版本")
            # with open(self.conf.UPDATE_FILE_PATH, 'w', encoding='utf8') as f:
            #     f.write("NULL")
            return

        logging.info('-*-'*10)
        # output update info
        for name, item in update_dict_info.items():
            logging.info("{} -- {}".format(name, item['tag']))
        temp = TEMPLATE(update_dict_info)
        msg = temp.template()

        # if self.conf.DELPOY_PLATFORM == "GITHUB_ACTION":
        #     with open(self.conf.UPDATE_FILE_PATH, 'w', encoding='utf8') as f:
        #         f.write(msg)
        #     logging.info("交由Github Action发送邮件")
        # else:
        #     data = {
        #         'receive': self.conf.MAIL['receivers'],
        #         'msg': msg,
        #         'type': 'html',
        #         'title': 'Github监控服务消息',
        #         'sender': self.conf.MAIL['email'],
        #         'password': self.conf.MAIL['password']
        #     }
        #     try:
        #         mail = QQMail(data)
        #         mail.send_email()
        #     except Exception as e:
        #         logging.error("发送邮件失败, {}".format(str(e)))
        #     else:
        #         logging.info("发送邮件成功！")
        data = {
            'receive': self.conf.MAIL['receivers'],
            'msg': msg,
            'type': 'html',
            'title': 'Github监控服务消息',
            'sender': self.conf.MAIL['email'],
            'password': self.conf.MAIL['password']
        }
        try:
            mail = QQMail(data)
            mail.send_email()
        except Exception as e:
            logging.error("发送邮件失败, {}".format(str(e)))
        else:
            logging.info("发送邮件成功！")
        logging.info('-*-'*10)
