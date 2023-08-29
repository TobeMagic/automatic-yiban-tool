#!user/bin/env python
import requests
import time
from lxml import etree
import json

root_url = "https://www.yooc.me"
headers = {
    'Cookie': "csrftoken=gCrVuIjnkv0KNIEfWXD6mV8znPrd5R5V; yiban_id=44944535; user_id=9449131; user_token=bfcd49e097c5f78bdf467f00c8279f5b; sessionid=bba84c1ee32863794f816807fa54f8cb; https_waf_cookie=ba305af0-87b1-4c57b9f5afcea6f88e641e7f524d322bf0bb",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

# session = requests.Session()
# resp = session.get(url="https://www.yooc.me/dashboard/mygroup", headers=headers)
# html = etree.HTML(resp.text)
# student_list = html.xpath("/html/body/section/section/section/div[2]/table/tr")

page1 = requests.get(url="https://www.yooc.me/group/managing?_=1678279258984&page=1", headers=headers)
page1_json = page1.json()
page2 = requests.get(url="https://www.yooc.me/group/managing?_=1678279258985&page=2", headers=headers)
page2_json = page2.json()
page3 = requests.get(url="https://www.yooc.me/group/managing?_=1678279258986&page=3", headers=headers)
page3_json = page3.json()

# all_json = {**page1_json, **page2_json}
class_url_name_dict = {}
all_item = page1_json["items"] + page2_json["items"] + page3_json["items"]
for item in all_item:
    class_url_name_dict[item['title']] = root_url + item['url']

# del all_item[-1]  # 删除不要的


for class_name in class_url_name_dict.keys():
    temp = class_url_name_dict[class_name]
    temp_res = requests.get(url=temp + "/topics", headers=headers)
    html = etree.HTML(temp_res.text)
    code = html.xpath('//*[@id="group-title"]/div[1]/div[1]/div[1]/p[1]/span//text()')[0]  # 获取不到原始信息？（删除掉tbody
    class_url_name_dict[class_name] = code
