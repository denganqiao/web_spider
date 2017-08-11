#!usr/bin/env python
#-*- coding:utf-8 -*-
"""
@author: Jeff Zhang
@date:   
"""
import scrapy


class DmozSpider(scrapy.Spider):
    name = 'dmoz'
    allowed_domains = ["dmoz.org"]

    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]


    def parse(self, response):
        filename = response.url.split("/")[-2]
        open(filename, 'wb').write(response.body)