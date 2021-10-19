from bs4 import BeautifulSoup
import requests
import urllib.request
import re
import os
from moviepy.editor import *


def wc(url):
    #params = {
    #    'param': 'arca.session2=M1LEp93sBv2Dtxqotw3hS2EGSDVBPk8y; arca.session2.sig=9NqhOmW0KxX3cIWHTGogKkdf56M; visited-channel=[{%22name%22:%22%EB%9D%BC%EC%8A%A4%ED%8A%B8%EC%98%A4%EB%A6%AC%EC%A7%84%22%2C%22slug%22:%22lastorigin%22}%2C{%22name%22:%22%EB%B2%A0%EC%8A%A4%ED%8A%B8%20%EB%9D%BC%EC%9D%B4%EB%B8%8C%22%2C%22slug%22:%22live%22}%2C{%22name%22:%22%EC%9D%B4%EC%99%9C%EC%A4%8C%22%2C%22slug%22:%22whyzoom%22}%2C{%22name%22:%22%EC%BB%B4%ED%93%A8%ED%84%B0%EA%B3%B5%ED%95%99%22%2C%22slug%22:%22programmers%22}%2C{%22name%22:%22%ED%85%8D%EC%8A%A4%ED%8A%B8%EA%B2%8C%EC%9E%84%22%2C%22slug%22:%22textgame%22}%2C{%22name%22:%22%EC%97%90%EC%96%B4%EC%86%8C%ED%94%84%ED%8A%B8%20%EA%B0%A4%EB%9F%AC%EB%A6%AC%22%2C%22slug%22:%22airsoft2077%22}%2C{%22name%22:%22%EC%9C%A0%EB%A0%89%EC%B9%B4%22%2C%22slug%22:%22iloveanimal%22}%2C{%22name%22:%22%EC%B9%B4%EC%9A%B4%ED%84%B0%EC%82%AC%EC%9D%B4%EB%93%9C%22%2C%22slug%22:%22counterside%22}%2C{%22name%22:%22%EB%AC%B8%EC%9D%98%20%EA%B2%8C%EC%8B%9C%ED%8C%90%22%2C%22slug%22:%22request%22}%2C{%22name%22:%22%EC%B1%84%EB%84%90%20%EB%AC%B8%EC%9D%98%20%EA%B2%8C%EC%8B%9C%ED%8C%90%22%2C%22slug%22:%22whyiblocked%22}%2C{%22name%22:%22%EA%B3%B5%EC%A7%80%EC%82%AC%ED%95%AD%22%2C%22slug%22:%22notice%22}%2C{%22name%22:%22%EC%9B%90%EC%8B%A0%22%2C%22slug%22:%22genshin%22}%2C{%22name%22:%22%EA%B5%AC%EB%8F%85%20%EC%A4%91%EC%9D%B8%20%EC%B1%84%EB%84%90%22%2C%22slug%22:%22my%22}%2C{%22name%22:%22%ED%8D%BC%EB%A6%AC%22%2C%22slug%22:%22furryshota%22}%2C{%22name%22:%22%ED%8C%8C%EC%9D%B4%EB%84%90%EA%B8%B0%EC%96%B4(%EC%A4%91%EC%9E%A5%EC%A0%84%ED%9D%AC)%22%2C%22slug%22:%22finalgear%22}%2C{%22name%22:%22%EC%8B%AC%EC%95%BC%EC%8B%9D%EB%8B%B9%22%2C%22slug%22:%22smpeople%22}%2C{%22name%22:%22%EC%86%8C%EC%9A%B8%EC%9B%8C%EC%BB%A4%22%2C%22slug%22:%22soulworkers%22}%2C{%22name%22:%22%EC%9E%AC%EB%AF%B8%EC%9E%88%EB%8A%94%20%EA%B2%8C%EC%8B%9C%ED%8C%90%22%2C%22slug%22:%22dogdrip%22}%2C{%22name%22:%22%EA%B2%8C%EC%9E%84%E2%80%8D%22%2C%22slug%22:%22cgame%22}%2C{%22name%22:%22%EC%97%90%ED%94%BD%EC%84%B8%EB%B8%90%22%2C%22slug%22:%22epic7%22}]; allow_sensitive_media=true; __cfduid=dd2cc0267b5f885165995b5c7208061e21620211312; arca.nick=%E3%85%87%E3%85%87; arca.nick.sig=ETcGz1yS4GbrdOJZZg18BIpnFrg; arca.password=512a0m2F; arca.password.sig=f5kj5YeizuQtteHak4Y8jCy8jEU'}

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
        pass
    else:
        os.makedirs("{}".format(title))

        for i in maintab:
            link = i.get('src')
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
                os.remove('{}/{}.{}'.format(title, count, filetype))
                count += 1
            else:
                with open('{}/{}.{}'.format(title, count, filetype), "wb") as file:
                    file.write(response.read())
                count += 1


def mp4togif(filename):
    clip = VideoFileClip(filename)
    rename = filename.replace('.mp4', '.gif')
    clip.write_gif(rename, fps=24, fuzz=1)
    return clip


if __name__ == '__main__':
    main('https://arca.live/e/5016?sort=rank&p=1')