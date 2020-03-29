import csv
from seleniumwire import webdriver
import time
import requests
from bs4 import BeautifulSoup
import json
from multiprocessing import Pool
from ip_read import get_proxy_ip


def read_csv(file):
	with open(file, 'r') as f:
		#order = ['good_id', 'pharm_id', 'offer_id', 'price', 'is_ad'] # определяем порядок чтения данных
		order = ['basket_onclick']
		listr = []
		reader = csv.DictReader(f, fieldnames=order)
		for item in reader:
			listr.append(item['basket_onclick'])
		chunks = [listr[x:x+15] for x in range(0, len(listr), 5)]
		#for it in chunks:
		selenium_mode(chunks[0])
		#with Pool(2) as p:
		#	result = p.map(selenium_mode, chunks)
		#return
		

def selenium_mode(orders):
	f = get_proxy_ip('ip_selenium.txt')
	wire_options = {
		'proxy':{
			'https': f,  #get_proxy_ip('ip_selenium.txt'),
			'http': f,
			}
		}
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	driver= webdriver.Chrome(seleniumwire_options=wire_options, options=options)
	driver.get('https://cenyvaptekah.ru/ufa/amoxicillin_kaps_500mg_n16')
	for item in orders:
		try:
			#driver.execute_script(f"Basket.clickBtnMoveToBasket({item['good_id']}, {item['pharm_id']}, {item['offer_id']}, {item['price']}, {item['is_ad']});")
			driver.execute_script(item)
		except:
			print('error')
		time.sleep(7)

	for request in driver.requests:
		if request.path == 'https://cenyvaptekah.ru/basket/add':
			cookie = {'cookie': request.headers['cookie']}
	get_basket(cookie)
	#driver.refresh()
	#request = driver.wait_for_request('https://cenyvaptekah.ru/city/ufa/pharm/basket/index_data', timeout=30)
	#for request in driver.requests:
	#	if request.path == 'https://cenyvaptekah.ru/city/ufa/pharm/basket/index_data':
	#		cookie = {'cookie': request.headers['cookie']}
	#		print('cookie')
	#		get_basket(cookie)
	#driver.quit()
	return



def get_basket(cookie):
	p = get_proxy_ip('ip_request.txt')
	proxy = { 'https' : p}
	url = 'https://cenyvaptekah.ru/city/ufa/pharm/basket/index_data'
	response = requests.get(url, params={'mode': 'full'}, cookies=cookie, proxies = proxy)
	data = response.json()['pharms']
	print(data)
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
			print(pharm)
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
	#cookie = {'cookie': '__cfduid=dafaacfc3a5b71c37163d86fd6ace5bcc1585429024; tval=top_buy; _PricesInPharm_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWRmM2UyNWFlZjYwYmQ1ODA4MGRhZjc2NTc4ZTZjNDM1BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMWxyM0xqNGVTaGdSWDA2VGJMSjM4UU1jUS9TTllTaStyVWYwejNEUUNOV1E9BjsARg%3D%3D--6fd72e80b95fa80143842181d64b199207c1871e; pharm_type=pharm; city=ufa; text=; isbliz=0; city_ufa_areas=; _ga=GA1.2.1785912785.1585429036; _gid=GA1.2.1182458319.1585429036; _ym_uid=1585429038120817515; _ym_d=1585429038; test=1; tmr_lvid=a6eac15eef6f58f5ee9150c02b9bdcd5; tmr_lvidTS=1585429042204; top100_id=t1.4469532.74438038.1585429042315; _ym_visorc_24215119=w; _ym_isad=2; __utma=265944989.1785912785.1585429036.1585429037.1585429037.1; __utmc=265944989; __utmz=265944989.1585429037.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); basket=eccd2aee-358c-4ca5-aaba-adc699e5b3a9; basket_hash=2603c440695df40f94b3339735e5cddf4f7b88b135f5fde4b80e1d17872b566e; tmr_detect=0%7C1585429606104; __utmt=1; __utmb=265944989.5.10.1585429037; tmr_reqNum=16; last_visit=1585411664162::1585429664162'}	
	#get_basket(cookie)
