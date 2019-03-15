#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import json
import random
import requests

# 正则提取 img src
img_pattern = re.compile(r'_WEBP \? "(.*?cc2)')

# 漫画地址
cartoon_url = 'http://manhua.163.com/reader/4942174423450126134/5297323304750041581#imgIndex=2@scale=7'

# 保存图片地址
save_img_url = r'img_url.txt'

# 保存图片文件夹
save_file_dir = r'E:\Mannix\reptile\netease_cartoon\img'

# 新建文件
os.makedirs(save_file_dir, exist_ok=True)

def download_img():
    num = 1
    with open(save_img_url, 'r') as f :
        for url in f:
            url = url.replace('\n', '')
            download = requests.get(url=url)
            img_html = download.content
            with open(save_file_dir + '/' + str(num) + '.jpg', 'wb+') as f:
                f.write(img_html)
            num += 1


def get_img_url():
    resp = requests.get(url=cartoon_url)
    img_url = img_pattern.findall(resp.text)
    for item in img_url:
        item = item.replace('? "', '')
        with open(save_file_die, 'a+') as f:
            f.write(item + '\n')

if __name__ == '__main__':
    download_img()

