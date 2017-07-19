#!usr/bin/env python
#-*- coding:utf-8 -*-
"""
@author: Jeff Zhang
@date:   2017-7-19
"""

import time
import datetime
import re
import urllib
from urllib import request
import itertools
from urllib import parse
import queue


def download(url, num_retries=5, user_agent='wswp', proxy=None):
    print('downloading:', url)
    headers = {'User-agent': user_agent}
    req = request.Request(url, headers=headers)
    opener = request.build_opener()
    if proxy:
        proxy_params = {parse.urlparse(url).scheme:proxy}
        opener.add_handler(request.ProxyHandler(proxy_params))
    try:
        html = request.urlopen(url).read()
    except request.URLError as e:
        print('download error:', e.reason)
        html = None
        if num_retries>0:
            if hasattr(e, 'code') and 500<=e.code<600:
                return download(url, num_retries-1)
    return html


def crawl_sitemap(url):
    sitemap = download(url).decode('utf-8')
    links = re.findall('a href="(.*?)"', sitemap)
    for link in links:
        html = download(url+link)

# crawl_sitemap("http://example.webscraping.com/sitemap.xml")


def spider_test(url):
    max_errors = 5
    num_errors = 0

    for page in itertools.count(1):
        url_ = url + '/-%d' % page
        html = download(url_)
        if html is None:
            num_errors += 1
            if num_errors == max_errors:
                break
        else:
            num_errors = 0


def link_crawler(seed_url, link_regex=None, delay=5, max_depth=1):
    crawl_queue = [seed_url]
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url).decode('utf-8')
        for link in get_links(html):
            if re.match(link_regex, link):
                link = parse.urljoin(seed_url, link)
                if link not in seen:
                    seen.add(link)
                    crawl_queue.append(link)


def get_links(html):
    webpage_regex = re.compile('a href="(.*?)"', re.IGNORECASE)

    return webpage_regex.findall(html)




class Throttle:

    def __init__(self, delay):
        self.delay = delay
        self.domains = {}

    def wait(self, url):
        domain = parse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.datetime.now()