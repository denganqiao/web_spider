# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class DingdianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    # 小说名
    name = Field()
    # 作者名
    author = Field()
    # 小说地址
    novelurl = Field()
    # 状态
    serialstatus = Field()
    # 连载数
    serialnumber = Field()
    # 文章类别
    category = Field()
    # 小说编号
    name_id = Field()



class DcontentItem(scrapy.Item):
    # 小说编号
    id_name = Field()
    # 章节内容
    chaptercontent = Field()
    # 用于绑定章节顺序
    num = Field()
    # 章节地址
    chapterurl = Field()
    # 章节名字
    chaptername = Field()


