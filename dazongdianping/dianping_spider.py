import urllib
from urllib import request
from bs4 import BeautifulSoup
import re
import json
import requests
from selenium import webdriver
import random
from requests import Session
import time


my_headers=[
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
]
    
random_header=random.choice(my_headers)


# 进入浏览器设置
options = webdriver.ChromeOptions()
random_header=random.choice(random_header)

# 更换头部
options.add_argument('user-agent=random_header')
options.add_argument('Host="www.dianping.com"')
options.add_argument('Connection="keep-alive"')
options.add_argument('Accept-Language="zh-CN,zh;q=0.8"')
# options.add_argument('--proxy-server=%s' % proxyip)
chrome_options = webdriver.ChromeOptions()
browser = webdriver.Chrome(chrome_options=options)

# 要抓取的目标网站地址
url = "https://www.dianping.com/shop/16789967"
try:
    browser.get(url)
except HTTPError as e:
    print(e)


html = browser.page_source
soup = BeautifulSoup(html, 'lxml')

# 经纬度
longitude = re.findall('shopGlng:"(.*?)",', str(soup))[0]
latitude = re.findall('shopGlat: "(.*?)",', str(soup))[0]

# 优惠促销
tuan_info = str()
cu_info = str()
huo_info = str()

try:
    elements = soup.find('div',{'id':'promoinfo-wrapper'}).findAll('div', {'class':'group clearfix'})
    for group in elements:
        for ele in group:
            if len(ele) > 1:
    #             print(ele)
                if ele.find('i').get_text() == u'团':
                    if ele.find('p', {'class':'title'}):
                        title = str(ele.find('p', {'class':'title'}).get_text()).split()[0]
                        current_price = ele.find('span', {'class':'price'}).get_text()
                        old_price = ele.find('del', {'class':'del-price'}).get_text()
                        sell_count = ele.find('span', {'class':'sold-count'}).get_text()
                        tuan_info += title+" 现价:"+current_price+" 原价:"+old_price+" "+sell_count+'   '
                    else:
                        title = str(re.findall('</del>(.*?)</a>', str(ele))[0]).split()[0]
                        current_price = ele.find('span', {'class':'price'}).get_text()
                        old_price = ele.find('del', {'class':'del-price'}).get_text()
                        tuan_info += title+" 现价:"+current_price+" 原价:"+old_price+"   "
                elif ele.find('i').get_text() == u'促':
                    cu = str(re.findall('</i>(.*?)</a>', str(ele))[0]).split()[0]
                    cu_info += cu
                elif ele.find('i').get_text() == u'活':
                    huo_info = None

    if tuan_info == '':
        tuan_info = u'无'
    if cu_info == '':
        cu_info = u'无'
    if huo_info == '':
        huo_info = u'无'

except:
    tuan_info = u'无'
    cu_info = u'无'
    huo_info = u'无'
    
# 订座信息
if soup.find('span', {"class":"desc"}):
    sit_info = soup.find('span', {"class":"desc"}).get_text()
else:
    sit_info = u'无'
    
# 推荐菜
recommend_food = str()
elements = soup.find('p', {"class":"recommend-name"}).findAll('a')
for ele in elements:
    food_info = ele.get_text().split()
    recommend_food += food_info[0]
    recommend_food += food_info[1]
    
    
# 特殊服务
try:
    special_elements = soup.find('p', {'class':'expand-info J-service nug-shop-ab-special_a'}).findAll('a')
    info_sp = re.findall('a class="tag tag-(.*?)-b', str(special_elements))
    sp_info = ""
    if info_sp:
        for ele in info_sp:
            if ele == "tuan":
                sp_info = sp_info + u"团 "
            elif ele == "wai":
                sp_info = sp_info + u"外 "
            elif ele == "cu":
                sp_info = sp_info + u"促 "
            elif ele == "ding":
                sp_info = sp_info + u"订 "
            elif ele == "huo":
                sp_info = sp_info + u"活 "
except:
    sp_info = u"无"
    
    
# 大家认为
comment = str()
try:
    
    comments = soup.find('div', {'class':'comment-condition J-comment-condition Fix'}).find('div', {'class':'conent'}).findAll('span')
    for ele in comments:
        comment += ele.get_text()
except:
    comment = u'无'
    
# 餐厅简介
try:
    soup.findAll('p', {'class':'info info-indent'})
    shop_brief_intro = soup.findAll('p', {'class':'info info-indent'})[1].get_text().strip()[5:]
except:
    shop_brief_intro = u'无'
    
# 时间
sell_time = str()
time_info = soup.find('p', {'class':'info info-indent'}).find('span', {'class':'item'}).get_text().split()
for ele in time_info:
    sell_time += ele
    sell_time += ' '
    
    
# 地址
address = soup.find('div', {'class':'expand-info address'}).find('span', {'class':'item'}).get_text().split()[0]

# 电话
tel = soup.find('p', {'class':'expand-info tel'}).find('span', {'class':'item'}).get_text()

# 分店数
try:
    soup.find('a', {'class':'branch J-branch'})
    other_shop_num = soup.find('a', {'class':'branch J-branch'}).get_text()[2:-3]
except:
    other_shop_num = 0
    
# 口味\环境\服务
scores = soup.find('div', {'class':'brief-info'}).find('span', {'id':'comment_score'}).findAll('span')
taste = scores[0].get_text()[3:]
environment = scores[1].get_text()[3:]
service = scores[2].get_text()[3:]

# 星级
rank = soup.find('div', {'class':'brief-info'}).find('span').attrs['title']

# 评论数
commend_num = soup.find('span', {'id':'reviewCount'}).get_text()

# id
shop_id = re.findall('[0-9]{1,}', url)[0]

# 店名
shop_name = soup.find('div', {'class':'breadcrumb'}).find('span').get_text()

# 菜系
try:
    food_type = soup.find('div', {'class':'breadcrumb'}).findAll('a')[2].get_text().split()[0]
except:
    food_type = u'无'
# 子菜系
try:
    sub_food_type = soup.find('div', {'class':'breadcrumb'}).findAll('a')[3].get_text().split()[0]
except:
    sub_food_type = u'无'
    
# 商圈
bc = soup.find('div', {'class':'breadcrumb'}).findAll('a')[1].get_text().split()[0]

# 城市
city = str(soup.find('a', {'class':'city J-city'}).get_text())

# 人均价格
price_info = soup.find('span', {'id':'avgPriceTitle'}).get_text()
pattern = re.compile('[0-9]{1,}')
result = pattern.findall(str(price_info))
avg_price = result[0]+u'元'

# 商户类型
shop_type = u'美食'


# 总信息
shop_info = {
    'city':city,
    'bc':bc,
    'shop_type':shop_type,
    'food_type':food_type,
    'sub_food_type':sub_food_type,
    'time':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),
    'url':url,
    'shop_id':shop_id,
    'shop_name':shop_name,
    'longitude':longitude,
    'latitude':latitude,
    'other_shop':other_shop_num,
    'rank':rank,
    'commend_num':commend_num,
    'avg_price':avg_price,
    'taste':taste,
    'environment':environment,
    'service':service,
    'address':address,
    'tel':tel,
    'special_service':sp_info,
    'tuan_info':tuan_info,
    'cu_info':cu_info,
    'huo_info':huo_info,
    'sit_info':sit_info,
    'recommend_food':recommend_food,
    'comment':comment
}
