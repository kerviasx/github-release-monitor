import os
import sys
import datetime
import logging
import warnings
import json
import platform

# Warning Settings
IGNORE_WARNING = True
if IGNORE_WARNING:
    warnings.filterwarnings('ignore')

# Thread number
THREAD_NUM = 10

# 需要监控的release地址
GITHUB_RELEASES = {
    "Qv2ray": "https://github.com/Qv2ray/Qv2ray/releases.atom",
    "QvPlugin-Trojan": "https://github.com/Qv2ray/QvPlugin-Trojan/releases.atom",
    "QvPlugin-Trojan-GO": "https://github.com/Qv2ray/QvPlugin-Trojan-Go/releases.atom",
    "QvPlugin-SSR": "https://github.com/Qv2ray/QvPlugin-SSR/releases.atom",
    "v2ray-core": "https://github.com/v2fly/v2ray-core/releases.atom",
    "xray-core": "https://github.com/XTLS/Xray-core/releases.atom",
    "Trojan-Go-core": "https://github.com/p4gefau1t/trojan-go/releases.atom",
    "ProxySU": "https://github.com/proxysu/windows/releases.atom",
    "lx-music": "https://github.com/lyswhut/lx-music-desktop/releases.atom",
    "hexo-next": "https://github.com/next-theme/hexo-theme-next/releases.atom",
    "Halo": "https://github.com/halo-dev/halo/releases.atom",
    "Traffic-Monitor": "https://github.com/zhongyang219/TrafficMonitor/releases.atom",
    "PicGo": "https://github.com/Molunerfinn/PicGo/releases.atom"
}

# 发送邮箱配置
MAIL = {
    "email": None,
    "password": None,
    "receivers": None
}

# Folder Path Settings
ROOT_FOLDER_PATH = os.path.realpath(os.path.dirname(os.path.abspath(sys.argv[0])))
LOG_FOLDER_PATH = ROOT_FOLDER_PATH + "/../log"
DATA_FOLDER_PATH = ROOT_FOLDER_PATH + "/../data"

sys = platform.system()
if sys == "Windows":
    LOG_FOLDER_PATH = ROOT_FOLDER_PATH + "/../log-win10"
    DATA_FOLDER_PATH = ROOT_FOLDER_PATH + "/../data-win10"

# File Path Settings
LOG_FILE_PATH = "{}/{}.log".format(LOG_FOLDER_PATH, datetime.datetime.now().strftime('%Y%m'))
DATA_FILE_PATH = DATA_FOLDER_PATH + '/result.json'

# PATH Check
if not os.path.exists(DATA_FOLDER_PATH):
    os.makedirs(DATA_FOLDER_PATH)

if not os.path.exists(LOG_FOLDER_PATH):
    os.makedirs(LOG_FOLDER_PATH)

if not os.path.exists(DATA_FILE_PATH):
    with open(DATA_FILE_PATH, 'w', encoding='utf8') as f:
        json.dump({}, f, indent=4, ensure_ascii=False)

# Logging Settings
sys = platform.system()
if sys != "Windows":
    file = open(LOG_FILE_PATH, encoding="utf-8", mode="a+")
    logging.basicConfig(stream=file, filemode="a+", format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)
else:
    logging.basicConfig(format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)

if MAIL['email'] is None or MAIL['password'] is None or MAIL['receivers'] is None:
    MAIL['email'] = os.environ.get('MAIL_USERNAME')
    MAIL['password'] = os.environ.get('MAIL_PASSWORD')
    MAIL['receivers'] = os.environ.get('MAIL_RECEIVERS')
    if MAIL['email'] is None or MAIL['password'] is None or MAIL['receivers'] is None:
        raise Exception("未指定邮箱配置")
    else:
        MAIL['receivers'] = MAIL['receivers'].split(',')
