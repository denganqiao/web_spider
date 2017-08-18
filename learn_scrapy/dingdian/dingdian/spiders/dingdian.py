import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
import sys
sys.path.append('../..')
from dingdian.items import DingdianItem


class Myspider(scrapy.Spider):
    name = 'dingdian'
    allowed_domains = ['x23us.com']
    bash_url = 'http://www.x23us.com/class/'
    bashurl = '.html'

    def start_requests(self):
        for i in range(1, 11):
            url = self.bash_url + str(i) + '_1' + self.bashurl
            yield Request(url, self.parse)
        yield Request('http://www.x23us.com/quanben/1', self.parse)

    def parse(self, response):
        max_num = BeautifulSoup(response.text, 'lxml').find('div', class_='pagelink').find_all('a')[-1].get_text()
        bashurl = str(response.url)[:-7]
        for num in range(1, int(max_num)+1):
            url = bashurl + '_' + str(num) + self.bashurl
            yield Request(url, callback=self.get_name)

    def get_name(self, response):
        tds = BeautifulSoup(response.text, 'lxml').find_all('tr', bgcolor='#FFFFFF')
        for td in tds:
            novelname = td.find('td', class_='L').find('a')['title'][0:-2]
            novelurl = td.find('td', class_='L').find('a')['href']
            novelauthor = td.find('td', class_='C').get_text()
            novelstatus = td.find_all('td', class_='C')[2].get_text()
            yield Request(novelurl, callback=self.chapterurl, meta={'name':novelname, 'url':novelurl, 'author':novelauthor, 'status':novelstatus})

    def chapterurl(self, response):
        item = DingdianItem()
        item['name'] = response.meta['name']
        item['novelurl'] = response.meta['url']
        item['author'] = response.meta['author']
        item['category'] = BeautifulSoup(response.text, 'lxml').find('table', bgcolor='#E4E4E4').find('a').get_text()
        item['name_id'] = response.meta['url'][-5:]
        item['serialstatus'] = response.meta['status']
        print(item)
        return item
