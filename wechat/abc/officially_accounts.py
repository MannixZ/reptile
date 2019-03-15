#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import time
import requests
from bs4 import BeautifulSoup

# 公众号基地址
# url = 'http://mp.weixin.qq.com/s/JHioeDcopm-98R5lGVemqw'
# url1 = 'http://mp.weixin.qq.com/s/x0wbU6i5WA_zRkW9mmvtrg'

# 公众号音频基地址
music_analysis_url = 'http://res.wx.qq.com/voice/getvoice'

# 公众号视频解析地址
vedio_analysis_url = 'http://v.ranks.xin/video-parse.php'

# 视频名称正则
vedio_name_pattern = re.compile(r'//.*/+(.*?).mp4')

# 视频内容文件夹
vedio_file = r'E:\Mannix\reptile\wechat\vedio_file'

# 音频内容文件夹
music_file = r'E:\Mannix\reptile\wechat\music_file'

# 图片内容文件夹
img_file = r'E:\Mannix\reptile\wechat\img_file'

def get_url_content(url):
    img_url = []
    music_url = []
    vedio_url = []

    # 获取文章title


    resp = requests.get(url=url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    # 获取文章标题
    title = soup.findAll('h2', attrs={'class':'rich_media_title'})[0].string.strip()
    print(title)


    # 获取图片链接
    imgs = soup.findAll('img', attrs={'data-copyright': '0'})
    if imgs is not None:
        for img in imgs:
            img = img['data-src']
            img_url.append(img)

    # 获取音频链接
    musics = soup.findAll('mpvoice')
    if musics is not None:
        for music in musics:
            music_key = music['voice_encode_fileid']
            music_url.append(music_key)


    # 获取视频链接
    vedios = soup.findAll('iframe', attrs={'frameborder': '0'})
    if vedios is not None:
        for vedio in vedios:
            vedio = vedio['data-src']
            vedio_url.append(vedio)

    return img_url, music_url, vedio_url

def get_vedio_download_url(vedio):
    headers = {
        'cache-control': "no-cache",
        'Postman-Token': "81266c29-1920-47d4-b9f9-1223655423aa"
    }
    print('开始解析视频链接:' + vedio)
    resp = requests.get(url=vedio_analysis_url, params={'url':vedio}, headers=headers)
    if resp is not None:
        resp_json = resp.json()
        vedio_download_url = resp_json['data'][0]['url']
        print('解析完成,开始下载视频:' + vedio_download_url)
        vedio_download = requests.get(url=vedio_download_url)
        if vedio_download is not None:
            vedio_name = re.findall(vedio_name_pattern, vedio_download_url)
            vedio_dir = os.makedirs(vedio_file, exist_ok=True)
            with open(vedio_file + '/' + vedio_name[0] + '.mp4', 'wb+') as f:
                f.write(vedio_download.content)
                print('视频下载完成:' + str(vedio_name))

def get_music_download_url(music):
    resp = requests.get(url=music_analysis_url, params={'mediaid':music})
    if resp is not None:
        music_name = str(int(time.time())) + '.mp3'
        print('开始下载音频:' + music_name)
        vedio_dir = os.makedirs(music_file, exist_ok=True)
        with open(music_file + '/' + music_name, 'wb+') as f:
            f.write(resp.content)
            print('音频下载完成:' + music_name)

def get_img_download_url(img):
    print('下载图片:' + img)
    resp = requests.get(url=img)
    if resp is not None:
        img_name = img.split('/')[-2]
        fmt = img.split('=')[-1]
        img_dir = os.makedirs(img_file, exist_ok=True)
        with open(img_file + '/' + img_name + '.' +fmt, 'wb+') as f:
            f.write(resp.content)

def main(url):
    img_url, music_url, vedio_url = get_url_content(url)
    for img in img_url:
        if img is not []:
            get_img_download_url(img)
    for music in music_url:
        if music is not []:
            get_music_download_url(music)
    for vedio in vedio_url:
        if vedio is not []:
            get_vedio_download_url(vedio)

if __name__ == '__main__':
    print('请输入你要抓取的微信文章链接:(输入Q回车或者按Ctrl+C退出~)')
    input_url = input()
    if input_url == 'Q':
        exit()
    else:
        main(input_url)