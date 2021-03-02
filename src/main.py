'''
    检测Github项目更新
'''

import conf.settings as CONFIG
import threadpool
from utils.parse import Settings
from spiders.GithubSpider import GithubReleaseSpider
import logging
import traceback


def main(conf):
    githubSpider = GithubReleaseSpider(conf)
    pool = threadpool.ThreadPool(CONFIG.THREAD_NUM)
    param_list = list(CONFIG.GITHUB_RELEASES.items())
    param_list = [[item[0], item[1]] for item in param_list]
    reqs = threadpool.makeRequests(githubSpider.spider, param_list)
    [pool.putRequest(req) for req in reqs]
    pool.wait()
    githubSpider.check_update_all()


if __name__ == '__main__':
    logging.info("Monitor Start")
    try:
        conf = Settings(CONFIG)
        main(conf)
    except Exception as e:
        logging.error(traceback.format_exc())
    logging.info("Monitor End\n")
