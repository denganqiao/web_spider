#!usr/bin/env python
#-*- coding:utf-8 -*-
"""
@author: James Zhang
@date:   
"""


from bs4 import BeautifulSoup
import time
import datetime
import re
import urllib
from urllib import request
import itertools
from urllib import parse



def download(url, num_retries=5, user_agent='wswp'):
    print('downloading:', url)
    headers = {'User-agent': user_agent}
    req = request.Request(url, headers=headers)
    try:
        html = request.urlopen(url).read().decode('utf-8')
    except request.URLError as e:
        print('download error:', e.reason)
        html = None
        if num_retries>0:
            if hasattr(e, 'code') and 500<=e.code<600:
                return download(url, num_retries-1)
    return html



url = 'http://example.webscraping.com/places/default/view/Afghanistan-1'
html = download(url)
soup = BeautifulSoup(html, 'lxml')
tr = soup.find(attrs={'id':'places_area__row'})
td = tr.find(attrs={'class':'w2p_fw'})
area = td.text
print(area)