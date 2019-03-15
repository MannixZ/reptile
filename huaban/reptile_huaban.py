#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import json
import requests

# 图片key输出地址
pin_ids_file = 'pin_ids.txt'

# 图片输出路径
pin_download_dit = r'E:/Mannix/reptile/img/'

# 图片下载地址
url = 'http://huaban.com/boards/29509610/'

# 图片打开地址
img_open_url = 'http://img.hb.aicdn.com/'

# 图片宽度
img_wide = '_fw658'

# 请求接口地址
req_url = 'http://huaban.com/boards/29509610/?jt5htuj1&max=2224430742&limit=20&wfl=1'

def get_boards_index_data(url):
    print('画板素材基地址: %s' %url)
    resp_content = requests.get(url=url)
    boards_pattern = re.compile(r'pins":(.*)};')
    result = boards_pattern.search(str(resp_content.text))
    json_dict = json.loads(result.group(1))
    for item in json_dict:
        with open(pin_ids_file, 'a') as f:
            f.write(item['file']['key'] + '\n')
    pin_id = json_dict[-1]['pin_id']
    return pin_id

def get_json_list(pin_id):
    req_url = url + '?jt5htuj1&max='+ str(pin_id) +'&limit=20&wfl=1'
    headers = headers = {
    'Host': "huaban.com",
    'Connection': "keep-alive",
    'Pragma': "no-cache",
    'Cache-Control': "no-cache",
    'Accept': "application/json",
    'X-Requested-With': "XMLHttpRequest",
    'X-Request': "JSON",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    'Referer': "http://huaban.com/boards/29509610/",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    'Cookie': "referer=https%3A%2F%2Fwww.google.com%2F; sid=e44jVqcNZssIO3JdhjMwrktWIMQ.uYHqT%2FWYEpy3Wjy5EFmCaqsQ5F%2FTwjGBsnKps42gbGo; _f=iVBORw0KGgoAAAANSUhEUgAAADIAAAAUCAYAAADPym6aAAABJElEQVRYR%2B1VOxYCIQwMF7KzsvFGXmW9kY2VnQfxCvgCRmfzCD9lnz53myWQAJOZBEfeeyIi7xz%2FyEXzZRPFhYbPc3hHXO6I6TbFixmfEyByeQQSxu6BcAXSkIGMazMjuBcz8pQcq44o0Iuyyc1p38C62kNsOdeSZDOQlLRQ80uOMalDgWCGMfsW2B5%2FATMUyGh2uhgptV9Ly6l5nNOa1%2F6zmjTqkH2aGEk2jY72%2B5k%2BNd9lBfLMh8GIP11iK95vw8uv7RQr4oNxOfbQ%2F7g5Z4meveyt0uKDEIiMLRC4jrG1%2FjkwKxCRE2e5lF30leyXYvQ628MZKV3q64HUFvnPAMkVuSWlEouLSiuV6dp2WtPBrPZ7uO5I18tbXWvEC27t%2BTcv%2Bx0JuJAoUm2L%2FQAAAABJRU5ErkJggg%3D%3D%2CWin32.1920.1080.24; BAIDU_SSP_lcr=https://www.google.com/; _uab_collina=155237152829647168256368; __auc=ebe0aa2d169708db412d41d12d7; UM_distinctid=169708db4b62cf-0f03f5ff98f931-9333061-1fa400-169708db4b7ab6; __gads=ID=93529f1f03e7e986:T=1552371528:S=ALNI_MYeDAdR4dQX4ehi1QFwT06FCVT5lg; Hm_lvt_d4a0e7c3cd16eb58a65472f40e7ee543=1552371529,1552371610; newbietask=1; registered=registered; uid=26512626; _tskw=1; __asc=613d9e3616971135e88abff5f06; CNZZDATA1256903590=730440136-1552368932-null%7C1552379732; Hm_lpvt_d4a0e7c3cd16eb58a65472f40e7ee543=1552380339; _cnzz_CV1256903590=is-logon%7Clogged-in%7C1552380339973%26urlname%7Cg0c9qctseog%7C1552380339973",
    'cache-control': "no-cache",
    'Postman-Token': "6eff617c-9b08-4d5f-9c4a-adb8b6decaba"
    }
    print('获取接口内容: %s' %req_url)
    resp = requests.get(url=req_url, headers=headers)
    json_resp = json.loads(resp.text)
    pins = json_resp['board']['pins']
    for item in pins:
        with open(pin_ids_file, 'a') as f:
            f.write(item['file']['key'] + '\n')
    return pins[-1]['pin_id']

def img_download():
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    with open(pin_ids_file, 'r') as f :
        for i in f:
            i = i.replace('\n', '')
            os.makedirs(pin_download_dit, exist_ok=True)
            img_html = requests.get(url=img_open_url + i + img_wide)
            with open(pin_download_dit + i + '.jpg', 'wb+') as f:
                f.write(img_html.content)
                print('下载图片: %s' %(img_open_url + i + img_wide))
    f.close()



def main():
    pin_id = get_boards_index_data(url)
    while True:
        try:
            pin_id = get_json_list(pin_id)
        except Exception as reason:
            break
    img_download()



if __name__ == '__main__':
    main()