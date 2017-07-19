# -*- coding: utf-8 -*-
# first web_spider

import string
from urllib import request

def baidu_tb(url, begin_page, end_page):
    for i in range(begin_page, end_page+1):
        sName = string.zfill(i, 5) + '.html'
        print('正在下载第' + str(i) + '个网页，并将其存储为' + sName + '.....')
        f = open(sName, 'w+')
        m = request.urlopen(url+str(i)).read()
        f.write(m)
        f.close()

bdurl = str(input(u'请输入贴吧地址：'))
begin_page = int(input(u'请输入开始的页数：'))
end_page = int(input(u'请输入终点的页数：'))


baidu_tb(bdurl, begin_page, end_page)
