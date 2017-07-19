#!usr/bin/env python
#-*- coding:utf-8 -*-
"""
@author: Jeff Zhang
@date:   2017-7-19
"""


import urllib
from urllib import request

def download(url, num_retries=5, user_agent='wswp'):
    print('downloading:', url)
    headers = {'User-agent': user_agent}
    req = request.Request(url, headers=headers)
    try:
        html = request.urlopen(url).read()
    except request.URLError as e:
        print('download error:', e.reason)
        html = None
        if num_retries>0:
            if hasattr(e, 'code') and 500<=e.code<600:
                return download(url, num_retries-1)
    return html

download('http://www.baiduxiswjocawoj.com')