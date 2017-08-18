import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
import sys
sys.path.append('../..')
from dingdian.items import DingdianItem, DcontentItem
sys.path.append('dingdian/mysqlpipelines')
from sql import Sql

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
            # novelstatus = td.find_all('td', class_='C')[2].get_text()
            yield Request(novelurl, callback=self.chapterurl, meta={'name':novelname,
                                                                    'url':novelurl,
                                                                    'author':novelauthor
                                                                    })

    def chapterurl(self, response):
        item = DingdianItem()
        item['name'] = response.meta['name']
        item['novelurl'] = response.meta['url']
        item['author'] = response.meta['author']
        item['category'] = BeautifulSoup(response.text, 'lxml').find('table', bgcolor='#E4E4E4').find('a').get_text()
        bash_url = BeautifulSoup(response.text, 'lxml').find('p', class_='btnlinks').find('a', class_='read')['href']
        name_id = str(bash_url)[-6:-1].replace('/', '')
        item['name_id'] = name_id
        # item['serialstatus'] = response.meta['status']
        yield item
        yield Request(bash_url, callback=self.get_chapter, meta={'name_id':name_id})


    def get_chapter(self, response):
        urls = re.findall('<td class="L"><a href="(.*?)">(.*?)</a></td>', response.text)
        num = 0
        for url in urls:
            num += 1
            chapterurl = response.url + url[0]
            chaptername = url[1]
            rets = Sql.select_chapter(chapterurl)
            if rets[0] == 1:
                print('章节已存在')
                pass
            else:
                yield Request(chapterurl, callback=self.get_chaptercontent, meta={'num':num,
                                                                              'name_id':response.meta['name_id'],
                                                                              'chaptername':chaptername,
                                                                              'chapterurl':chapterurl
                                                                              })

    def get_chaptercontent(self, response):
        item = DcontentItem()
        item['num'] = response.meta['num']
        item['id_name'] = response.meta['name_id']
        item['chaptername'] = str(response.meta['chaptername']).replace('\xa0', '')
        item['chapterurl'] = response.meta['chapterurl']
        content = BeautifulSoup(response.text, 'lxml').find('dd', id='contents').get_text()
        item['chaptercontent'] = str(content).replace('\xa0', '')
        return item