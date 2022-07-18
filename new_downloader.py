# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import urllib.request
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import concurrent.futures
import time

def wc(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"}
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "lxml")
    return soup


def imgLinkListReturn(url):
    soup = wc(url)
    detail = soup.find('div','emoticons-wrapper')
    maintab = detail.find_all(loading='lazy')
    imgLinkList = []

    for i in maintab:
        link = i.get('src')
        if link is None:
            link = i.get('data-src')
        imgLinkList.append(f"http://{link[2:]}")

    return imgLinkList


def imgDownload(imglist):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"}
    title = imglist[0]
    imglink = imglist[1]

    request_ = urllib.request.Request(imglink, None, headers)
    response = urllib.request.urlopen(request_)
    result = imglink.split('.')
    filetype = ''.join(result[-1])

    filenamelist = imglink.split('/')
    filename = filenamelist[-1][:-4]

    if filetype == 'mp4':
        with open('{}/{}.{}'.format(title, filename, filetype), "wb") as file:
            file.write(response.read())
        mp4togif('{}/{}.{}'.format(title, filename, filetype))
        print(f"{filename}")
    else:
        with open('{}/{}.{}'.format(title, filename, filetype), "wb") as file:
            file.write(response.read())
            print(f"{filename}")



def mp4togif(filename):
    clip = VideoFileClip(filename)
    rename = filename.replace('.mp4', '.gif')
    clip.write_gif(rename, fps=30, fuzz=1)
    return clip


def remover(filepath):
    filelist = os.listdir(filepath)
    for file in filelist:
        if 'mp4' in file:
            try:
                os.remove(f"{filepath}/{file}")
            except:
                print('mp4파일 삭제 오류')
        else:
            pass

def con_downloader():
    while 1:
        conUrl = input("원하는 콘 url을 입력하세요(종료하려면 q를 입력): ")
        if conUrl == 'q' or conUrl == 'Q' or conUrl == 'ㅂ':
            break
        else:
            try:
                soup = wc(conUrl)
                title = soup.find('div', 'title-row').text.strip()
                result = [[title, link] for link in imgLinkListReturn(conUrl)]
                if os.path.exists("{}".format(title)):
                    print('이미 존재하는 콘')
                else:
                    os.makedirs("{}".format(title))
                    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                        executor.map(imgDownload, result)
                    remover(f"{title}")

            except:
                print('유효하지 않은 url이거나 잘못된 url')


if __name__ == '__main__':
    con_downloader()





