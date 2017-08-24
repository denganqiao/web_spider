#!usr/bin/env python
#-*- coding:utf-8 -*-
"""
@author: Jeff Zhang
@date:   
"""

from news_spider.items import NewsItem

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
import json
import re
from scrapy import Request

def ListCombiner(lst):
    string = ""
    for e in lst:
        string += e
    return string.replace(' ','').replace('\n','').replace('\t','').replace('\xa0','')


class NeteaseNewsSpider(CrawlSpider):
    name = "netease_news_spider"
    # allowed_domains = ['news.163.com']
    start_urls = ['http://news.163.com/']

    # http://news.163.com/17/0823/20/CSI5PH3Q000189FH.html
    url_pattern = r'(http://news\.163\.com)/(\d{2})/(\d{4})/\d+/(\w+)\.html'
    rules = [Rule(LxmlLinkExtractor(allow=[url_pattern]), callback='parse_news', follow=True)]

    def parse_news(self, response):
        sel = Selector(response)
        pattern = re.match(self.url_pattern, str(response.url))
        source = 'news.163.com'
        date = '20' + pattern.group(2) + '/' + pattern.group(3)[0:2] + '/' + pattern.group(3)[2:]
        newsId = pattern.group(4)
        url = response.url
        title = sel.xpath("//h1/text()").extract()[0]
        contents = ListCombiner(sel.xpath('//p/text()').extract()[2:-3])
        comment_url = 'http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/{}'.format(newsId)
        yield Request(comment_url, self.parse_comment, meta={'source':source,
                                                             'date':date,
                                                             'newsId':newsId,
                                                             'url':url,
                                                             'title':title,
                                                             'contents':contents,
                                                             })
        # return item

    def parse_comment(self, response):
        result = json.loads(response.text)
        item = NewsItem()
        item['source'] = response.meta['source']
        item['date'] = response.meta['date']
        item['newsId'] = response.meta['newsId']
        item['url'] = response.meta['url']
        item['title'] = response.meta['title']
        item['contents'] = response.meta['contents']
        item['comments'] = result['cmtAgainst'] + result['cmtVote'] + result['rcount']
        return item






class TencentNewsSpider(CrawlSpider):
    name = "tencent_news_spider"
    pass


class SohuNewsSpider(CrawlSpider):
    name = "sohu_news_spider"
    pass