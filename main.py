'''
    检测Github项目更新
'''

import conf.settings as CONFIG
import threadpool
from utils.parse import Settings
from spiders.GithubSpider import GithubReleaseSpider
import logging

def main(conf):
    githubSpider = GithubReleaseSpider(conf)
    pool = threadpool.ThreadPool(CONFIG.THREAD_NUM)
    reqs = threadpool.makeRequests(githubSpider.spider, githubSpider.get_monitor_urls())
    [pool.putRequest(req) for req in reqs]
    pool.wait()
    githubSpider.save_result()


if __name__ == '__main__':
    logging.info("Monitor Start")
    conf = Settings(CONFIG)
    main(conf)
    logging.info("Monitor End\n")
