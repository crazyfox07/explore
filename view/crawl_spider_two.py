# -*- coding:utf-8 -*-
"""
File Name: crawl_spider
Version:
Description:
Author: liuxuewen
Date: 2017/8/11 9:50
"""

from bs4 import BeautifulSoup
import time
from model.huanqiu_model import HuanQiuOrm, db_session
import uuid
import requests
import os

from view.util.redis_api import exists_url_hash, add_url_hash


def func(item):
    if item.find('img'):
        img_url = item.find('img')['src']
        img_name = uuid.uuid4().hex
        file_path = '{}/static/imgs/{}.png'.format(os.path.dirname(os.path.dirname(__file__)), img_name)
        with open(file_path, 'wb') as f:
            content = requests.get(img_url).content
            f.write(content)
        try:
            return item.select('h3 a')[0]['title'], item.select('h3 a')[0]['href'], item.select('h5')[
                0].text.strip(), item.find('h6').text.strip(), file_path
        except:
            return None

    else:
        try:
            return item.select('h3 a')[0]['title'], item.select('h3 a')[0]['href'], item.select('h5')[
                0].text.strip(), item.find('h6').text.strip(), ''
        except:
            return None


class Crawl_HuanQiu(object):
    def __init__(self):
        start_url = 'http://tech.huanqiu.com/discovery/'

    def store_db(self, item):
        if not item:
            return
        title = item[0][:64]
        link = item[1][:64]
        brief = item[2][:64]
        create_time = item[3]
        img_url = item[4]
        if not exists_url_hash(link):
            db_session.add(HuanQiuOrm(title=title,
                                      link=link,
                                      brief=brief,
                                      create_time=create_time,
                                      img_url=img_url))
            db_session.commit()
            db_session.close()
            add_url_hash(link)

    def parse_html(self, soup):
        items = soup.find('ul', class_='listPicBox').find_all('li', class_='item')
        results = map(func, items)
        [self.store_db(item) for item in results]

    def crawl(self, url):
        res = requests.get(url)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'lxml')
        self.parse_html(soup)


def crawl_huanqiu():
    url = 'http://tech.huanqiu.com/discovery/'
    hq = Crawl_HuanQiu()
    begin = time.time()
    urls = []
    urls.extend(['{}/{}.html'.format(url, page) for page in range(2, 10)])
    [hq.crawl(url) for url in urls]
    end = time.time()
    print('time use:  {} '.format(end - begin))


if __name__ == '__main__':
    crawl_huanqiu()
    # a=uuid.uuid4().hex
    # print(a)
    # print(len('D:/project/flask_project/explore/static/imgs/8daf0f2b668849e8b38825b5ab775338.png'))
