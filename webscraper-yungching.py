import requests
from fake_useragent import UserAgent
from bs4 import  BeautifulSoup as bs
import pandas as pd
import time,random

ua = UserAgent()
headers = {
    'user-agent': ua.random
}

url_yungching = 'https://buy.yungching.com.tw/region/%E4%BD%8F%E5%AE%85_p/%E6%96%B0%E5%8C%97%E5%B8%82-%E6%9E%97%E5%8F%A3%E5%8D%80_c/_rm/?pg=1'
response_yungching = requests.get(url_yungching, headers=headers)
cookies = response_yungching.cookies.get_dict()
jar = requests.utils.cookiejar_from_dict(cookies)

rs = requests.session()
soup_all = []
for page in range(1,11):
    url = f'https://buy.yungching.com.tw/region/%E4%BD%8F%E5%AE%85_p/%E6%96%B0%E5%8C%97%E5%B8%82-%E6%9E%97%E5%8F%A3%E5%8D%80_c/_rm/?pg={page}'
    response_yungching = rs.get(url, headers=headers, cookies=jar)
    soup_yungching = bs(response_yungching.text, 'lxml')
    for item in soup_yungching.find_all('li',{'class':'m-list-item'}):
        soup_all.append(item)
    time.sleep(random.uniform(1,4))

base_url = 'https://buy.yungching.com.tw'
title = [i.find('a', {'class':'item-title ga_click_trace'}).find('h3').text for i in soup_all]
urls = [base_url + i.find('div', {'class':'item-info'}).a['href'] for i in soup_all]
addr = [i.find('div', {'class':'item-description'}).find('span').text for i in soup_all]
house_type = [i.find('ul', {'class':'item-info-detail'}).find_all('li')[0].text for i in soup_all ]
house_age = [i.find('ul', {'class':'item-info-detail'}).find_all('li')[1].text.strip().replace('年','') for i in soup_all ]
floor = [i.find('ul', {'class':'item-info-detail'}).find_all('li')[2].text.strip().replace('樓','') for i in soup_all ]
land = [i.find('ul', {'class':'item-info-detail'}).find_all('li')[3].text.replace('坪', '').replace('土地 ', '') for i in soup_all ]
build = [i.find('ul', {'class':'item-info-detail'}).find_all('li')[5].text.replace('建物 ','').replace('坪', '') for i in soup_all ]
pattern = [i.find('ul', {'class':'item-info-detail'}).find_all('li')[6].text.strip() for i in soup_all ]
parking = [i.find('ul', {'class':'item-info-detail'}).find_all('li')[8].text.strip().replace('(含車位','').replace('坪)','') for i in soup_all ]

dict_yungchinng = {}
dict_yungchinng['物件名稱'] = title
dict_yungchinng['網址'] = urls
dict_yungchinng['路段'] = addr
dict_yungchinng['類型'] = house_type
dict_yungchinng['屋齡'] = house_age
dict_yungchinng['樓層'] = floor
dict_yungchinng['土地坪數'] = land
dict_yungchinng['房廳格局'] = pattern
dict_yungchinng['車位'] = parking

df_yungching = pd.DataFrame(dict_yungchinng)
df_yungching