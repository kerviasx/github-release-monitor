import requests
import xml.dom.minidom as minidom
import json
import queue
import threading
import logging
import traceback

from utils.template import TEMPLATE
from utils.mail import QQMail

class GithubReleaseSpider(object):
    def __init__(self, conf):
        self.conf = conf
        self.queue = queue.Queue()
        self.history_info = {}
        self.init_history_info()


    def init_history_info(self):
        try:
            self.history_info = json.load(open(self.conf.DATA_FILE_PATH, 'r', encoding='utf8'))
        except Exception as e:
            self.history_info = {}


    def spider(self, item):
        th_id = threading.currentThread().ident
        name, url = item[0], item[1]
        logging.info("[ID={}]:{}->{}".format(th_id, item[0], item[1]))

        headers = {
            'accept-language': 'zh-CN,zh;q=0.9',
            # 'content-type': 'text/html; charset=UTF-8',
            # 'accept': 'text/html',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }

        resp = None
        result = None
        try:
            s = requests.session()
            s.headers.update(headers)
            s.keep_alive = False
            resp = s.get(url, verify=False)
            s.close()
            result = self.parse_response(resp)
        except Exception as e:
            logging.error("[ID={}]:{}".format(th_id, traceback.format_exc()))

        self.queue.put((name, result))

    def parse_response(self, resp):
        root = minidom.parseString(resp.text)
        entries = root.getElementsByTagName('entry')
        if len(entries) == 0:
            return None
        
        entry = entries[0]
        tag = entry.getElementsByTagName("id")[0].childNodes[0].data.split("/")[-1]
        time = entry.getElementsByTagName("updated")[0].childNodes[0].data
        link = entry.getElementsByTagName("link")[0].getAttribute("href")
        title = entry.getElementsByTagName("title")[0].childNodes[0].data
        content = entry.getElementsByTagName("content")[0].childNodes[0].data

        return {
            'tag': tag,
            'title': title,
            'content': content,
            'url': link,
            'time': time
        }
    
    def check_update_all(self):
        size = self.queue.qsize()
        new_info_dict = dict([self.queue.get() for i in range(size)])
        old_info_dict = self.history_info
        update_info_dict = {}
        file_info_dict = {}
        flag = False
        for k,v in new_info_dict.items():
            if v != None:
                file_info_dict[k] = v
                if k not in old_info_dict.keys() or old_info_dict[k]['time'] != new_info_dict[k]['time']:
                    flag = True
            elif k in old_info_dict.keys():
                file_info_dict[k] = old_info_dict[k]
            if v == None: # 获取信息失败的
                new_info_dict[k] = {
                    'tag': "No Tag",
                    'title': k,
                    'content': "获取信息失败",
                    'url': "ss",  #self.conf.GITHUB_RELEASES[k],
                    'time': ''
                }
            if k not in old_info_dict.keys():
                update_info_dict[k] = new_info_dict[k]
            elif old_info_dict[k]['time'] != new_info_dict[k]['time']:
                update_info_dict[k] = new_info_dict[k]
        
        if flag:
            with open(self.conf.DATA_FILE_PATH, 'w', encoding='utf8') as f:
                json.dump(file_info_dict, f, indent=4, ensure_ascii=False)
        
        if len(update_info_dict) != 0:            
            self.send_email(update_info_dict)


    def send_email(self, update_info_dict):
        logging.info('-*-'*10)
        # output update info
        for name, item in update_info_dict.items():
            logging.info("{} -- {}".format(name, item['tag']))
        temp = TEMPLATE(update_info_dict)
        msg = temp.template()

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
            #mail.send_email()
        except Exception as e:
            logging.error("发送邮件失败, {}".format(str(e)))
        else:
            logging.info("发送邮件成功！")
        logging.info('-*-'*10)

        

if __name__ == "__main__":
    github = GithubReleaseSpider(None)
    github.spider(('ProxySU', 'https://github.com/proxysu/ProxySU/releaes.atom'))
    github.check_update_all()
    
