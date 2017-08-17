#!usr/bin/env python
#-*- coding:utf-8 -*-
"""
@author: James Zhang
@date:   
"""

import urllib
from urllib.request import urlopen
import requests
import json
from bs4 import BeautifulSoup
import demjson
from pprint import pprint


url = 'http://www.foods12331.cn/food/detail/findFoodByPage'
headers = {
    'Accept':'application/json',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Cookie':'CA0AE10AB2A6BFCF4D518AB76F3F0DBD',
    'Host':'www.foods12331.cn',
    'Origin':'http://www.foods12331.cn',
    'Referer':'http://www.foods12331.cn/web/index.jsp?food_type=%E9%A5%AE%E6%96%99',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'X-Request':'JSON',
    'X-Requested-With':'XMLHttpRequest'
}
s = requests.session()
data = {
    'filters':'"food_type":"粮食加工品","check_flag":"合格","order_by":"1","pageNo":7,"pageSize":20,"bar_code":"","sampling_province":"","name_first_letter":null,"food_name":null}'
}

html = s.post(url=url, data=json.dumps(data), headers=headers)


print(html.text)