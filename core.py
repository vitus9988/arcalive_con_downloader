# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import urllib.request
from moviepy.video.io.VideoFileClip import VideoFileClip
import os

def wc(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"}
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "lxml")
    return soup


def main(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"}

    soup = wc(url)
    title = soup.find('div','title-row').text.strip()
    detail = soup.find('div','emoticons-wrapper')
    maintab = detail.find_all(loading='lazy')
    count = 1

    if os.path.exists("{}".format(title)):
        print('이미 존재하는 콘')
    else:
        os.makedirs("{}".format(title))

        for i in maintab:
            link = i.get('src')
            if link is None:
                link = i.get('data-src')

            print("http://{}".format(link[2:]))
            imglink = "http://{}".format(link[2:])
            request_ = urllib.request.Request(imglink, None, headers)
            response = urllib.request.urlopen(request_)

            result = imglink.split('.')
            filetype = ''.join(result[-1])

            if filetype == 'mp4':
                with open('{}/{}.{}'.format(title, count, filetype), "wb") as file:
                    file.write(response.read())
                mp4togif('{}/{}.{}'.format(title, count, filetype))
                count += 1
            else:
                with open('{}/{}.{}'.format(title, count, filetype), "wb") as file:
                    file.write(response.read())
                count += 1

    remover(f"{title}")


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



def con_download():
    while 1:
        conUrl = input("원하는 콘 url을 입력하세요(종료하려면 q를 입력): ")
        if conUrl == 'q' or conUrl == 'Q' or conUrl == 'ㅂ':
            break
        else:
            try:
                main(conUrl)
            except:
                print('유효하지 않은 url이거나 잘못된 url')


if __name__ == '__main__':
    #main('https://arca.live/e/56?target=title&keyword=%EB%9D%BC%EC%98%A4&sort=rank&p=1')
    con_download()