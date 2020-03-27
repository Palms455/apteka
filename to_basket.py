import csv
from seleniumwire import webdriver
import time
import requests
from bs4 import BeautifulSoup
import json
from multiprocessing import Pool


def read_csv(file):
	with open(file, 'r') as f:
		#order = ['good_id', 'pharm_id', 'offer_id', 'price', 'is_ad'] # определяем порядок чтения данных
		order = ['basket_onclick']
		listr = []
		reader = csv.DictReader(f, fieldnames=order)
		for item in reader:
			listr.append(item['basket_onclick'])
		chunks = [listr[x:x+15] for x in range(0, len(listr), 5)]
		with Pool(8) as p:
			result = p.map(selenium_mode, chunks)
		return
		

def selenium_mode(orders):
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	driver= webdriver.Chrome(options=options)
	driver.get('https://cenyvaptekah.ru/ufa/supradin_tabletki_shipuchie_10_sht_')
	for item in orders:
		try:
			#driver.execute_script(f"Basket.clickBtnMoveToBasket({item['good_id']}, {item['pharm_id']}, {item['offer_id']}, {item['price']}, {item['is_ad']});")
			driver.execute_script(item)
		except:
			print('error')
		time.sleep(4)

	driver.refresh()
	for request in driver.requests:
		if request.response:
			if request.path == 'https://cenyvaptekah.ru/city/ufa/pharm/basket/index_data':
				cookie = {'cookie': request.headers['cookie']}
				get_basket(cookie)
	driver.quit()
	return



def get_basket(cookie):
	url = 'https://cenyvaptekah.ru/city/ufa/pharm/basket/index_data'
	response = requests.get(url, params={'mode': 'full'}, cookies=cookie)
	data = response.json()['pharms']
	for pharm_data in data:
		apteka = pharm_data['pharm_data']['name'] + pharm_data['pharm_data']['address']
		for drug in pharm_data['goods']:
			pharm_name = drug['good_name']
			price = drug['price']
			quantity = drug['rest']
			pharm = {'pharm_name': pharm_name,
					'pharm_adres': apteka,
					'price': price,
					'quantity': quantity,
					}
			write_csv(pharm)
	return

			
		
def write_csv(data):
		with open('Pharm.csv', 'a',encoding='utf-8') as file:
			order = ['pharm_name', 'pharm_adres', 'price', 'quantity']
			writer = csv.DictWriter(file, fieldnames=order)
			writer.writerow(data)
		return



if __name__ == '__main__':
	tic = time.time()
	read_csv('goods_id.csv')
	toc = time.time()
	print(toc - tic)
