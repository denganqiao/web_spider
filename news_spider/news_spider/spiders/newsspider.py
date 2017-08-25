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
    return string.replace(' ','').replace('\n','').replace('\t','').replace('\xa0','').replace('\u3000','')


class NeteaseNewsSpider(CrawlSpider):
    name = "netease_news_spider"
    allowed_domains = ['news.163.com']
    start_urls = ['http://news.163.com/']

    # http://news.163.com/17/0823/20/CSI5PH3Q000189FH.html
    url_pattern = r'(http://news\.163\.com)/(\d{2})/(\d{4})/\d+/(\w+)\.html'
    rules = [
        Rule(LxmlLinkExtractor(allow=[url_pattern]), callback='parse_news', follow=True)
    ]

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



class SinaNewsSpider(CrawlSpider):
    name = "sina_news_spider"
    allowed_domains = ['news.sina.com.cn']
    start_urls = ['http://news.sina.com.cn']
    # http://finance.sina.com.cn/review/hgds/2017-08-25/doc-ifykkfas7684775.shtml
    url_pattern = r'(http://(?:\w+\.)*news\.sina\.com\.cn)/.*/(\d{4}-\d{2}-\d{2})/doc-(.*)\.shtml'
    # url_pattern = r'(http://(?:\w+\.)*news\.sina\.com\.cn)/.*/(2017-08-25)/doc-(.*)\.shtml'

    rules = [
        Rule(LxmlLinkExtractor(allow=[url_pattern]), callback='parse_news', follow=True)
    ]

    def parse_news(self, response):
        sel = Selector(response)
        if sel.xpath("//h1[@id='artibodyTitle']/text()"):
            title = sel.xpath("//h1[@id='artibodyTitle']/text()").extract()[0]
            pattern = re.match(self.url_pattern, str(response.url))
            source = 'news.sina.com.cn'
            date = pattern.group(2).replace('-','/')
            newsId = pattern.group(3)
            url = response.url
            contents = ListCombiner(sel.xpath('//p/text()').extract()[:-3])
            comment_elements = sel.xpath("//meta[@name='sudameta']").xpath('@content').extract()[1]
            comment_channel = comment_elements.split(';')[0].split(':')[1]
            comment_id = comment_elements.split(';')[1].split(':')[1]
            comment_url = 'http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel={}&newsid={}'.format(comment_channel,comment_id)
            yield Request(comment_url, self.parse_comment, meta={'source':source,
                                                                 'date':date,
                                                                 'newsId':newsId,
                                                                 'url':url,
                                                                 'title':title,
                                                                 'contents':contents,
                                                                })

    def parse_comment(self, response):
        if re.findall(r'"total": (\d*)\,', response.text):
            comments = re.findall(r'"total": (\d*)\,', response.text)[0]
        else:
            comments = 0
        item = NewsItem()
        item['comments'] = comments
        item['title'] = response.meta['title']
        item['url'] = response.meta['url']
        item['contents'] = response.meta['contents']
        item['source'] = response.meta['source']
        item['date'] = response.meta['date']
        item['newsId'] = response.meta['newsId']
        return item


class TencentNewsSpider(CrawlSpider):
    name = "tencent_news_spider"
    pass


class SohuNewsSpider(CrawlSpider):
    name = "sohu_news_spider"
    pass







