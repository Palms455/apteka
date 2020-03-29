import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import json
import time
import csv
from random import choice, randint
from fake_useragent import UserAgent
from ip_read import get_proxy_ip


ua = UserAgent()


def get_html(url):
	headers = {
	'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'cookie': '__cfduid=d3e953c1c16bab30aa7a99d46eb99956f1585210471; tval=top_buy_none; city_ufa_areas=; pharm_type=pharm; city=ufa; text=; _ga=GA1.2.616775817.1585210492; _gid=GA1.2.683288620.1585210492; _ym_uid=1585210492209663619; _ym_d=1585210492; test=1; _ym_visorc_24215119=w; __utma=265944989.616775817.1585210492.1585210493.1585210493.1; __utmc=265944989; __utmz=265944989.1585210493.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; tmr_lvid=1864951ad57915a00afe8960898f0fa4; tmr_lvidTS=1585210493994; _ym_isad=2; top100_id=t1.4469532.2009364880.1585210495863; _PricesInPharm_session=BAh7DEkiD3Nlc3Npb25faWQGOgZFVEkiJTE4ZGY0YWI1YTBiOGFmYmI0ZmM4YzU5YTlmYjc4MTJlBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMWsyU0NrYm1MQ20yTEpXbXB1YitDY0FtSHRDZlNCV1cxREJKSXd4Ri9rM3c9BjsARkkiB3N0BjsARkkiDzE1ODUyMTA1MjIGOwBGSSIHY3QGOwBGSSIPMTU4NTIxMDUyMgY7AEZJIgZxBjsARkkiBjAGOwBGSSIHcWEGOwBGSSIGMAY7AEZJIgZhBjsARkkiB1tdBjsAVA%3D%3D--59cefb3415b13c461ac32ec4827d470656a85539; _gat_gtag_UA_48328690_1=1; __utmb=265944989.5.10.1585210493; last_visit=1585192555618::1585210555618; tmr_detect=0%7C1585210559814; tmr_reqNum=16',
	'origin': 'https://cenyvaptekah.ru',
	'pragma': 'no-cache',
	'referer': 'https://cenyvaptekah.ru/ufa/',
	'sec-fetch-dest': 'empty',
	'sec-fetch-mode': 'cors',
	'sec-fetch-site': 'same-origin',
	#'user-agent': ua.random,
	#'x-csrf-token': 'hev5isie5ANSX51IE4YRVpJeYIZK1jbTYrnZCqp9M1k=',
	#'x-requested-with': 'XMLHttpRequest',
	}

	p = get_proxy_ip('ip_request.txt')
	proxy = { 'https' : p}
	print(proxy)
	#user_agent = { 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Mobile Safari/537.36'}
	try:
		r = requests.get(url, proxies=proxy, headers=headers)
		print(r.status_code)
	except:
		print('bad request. retrying')
		return get_html(url)
	if r.status_code == 200:
		print('ok')
		return r.text
	else: get_html(url)


def get_data(html):
	links = set()
	soup = BeautifulSoup(html, 'lxml')
	link_goods = soup.find_all('a', class_='nodecor')
	for i in link_goods:
		#print(i)
		if '0.00 руб.' not in i.find('span', class_='price_grid').text:
			links.add(('https://cenyvaptekah.ru' + i.get('href')))
	return links

def link_pool(html):
	link_goods = set()
	soup = BeautifulSoup(html, 'lxml')
	groups = soup.find_all('div', {'class': 'span4 mb-10'})
	for item in groups:
		#time.sleep(randint(1,6))
		links = 'https://cenyvaptekah.ru' + item.find('a').get('href')
		print(links)
		urls = get_data(get_html(links)) #собираем url внутри группы
		if urls:
			link_goods = link_goods.union(urls) # все ссылки на товары
	print('all urls added!')
	with Pool(20) as p:
		results = p.map(make_all, link_goods)
	#for link in link_goods:
	#	print(link)
	#	time.sleep(randint(2,8))
	#	offers(get_html(link))
	return

def make_all(link):
	html = get_html(link)
	return offers(html)		

def offers(html):
	add_params = {}
	goods = []
	print('in offers')
	#response = requests.get(link)
	#print(response.status_code)
	data = BeautifulSoup(html, 'lxml')
	basket = data.select('.row-fluid>.buy-btn-div>a.btn.btn-info')
	for item in basket:
		basket_onclick = item.get('onclick')
		#dat = item.get('onclick')[28:-1].split(',')
		#add_params['good_id'] = dat[0]
		#add_params['pharm_id'] = dat[1]
		#add_params['offer_id'] = dat[2]
		#add_params['price'] = dat[3]
		#add_params['is_ad'] = dat[4]
		#goods.append(add_params)
		goods.append(basket_onclick)
		write_csv({'basket_onclick' : basket_onclick}, 'goods_id')
		print('write good_id')
	return goods 


		
def write_csv(data, name):
	with open(f'{name}.csv', 'a',encoding='utf-8') as file:
		writer = csv.DictWriter(file, fieldnames=['basket_onclick'])
		writer.writerow(data)
		



if __name__ == '__main__':
	tic = time.time()
	#cookie = {'cookie': '__cfduid=d62fe2da8ffeb7073f3e8ba82c4b17c561584629759; tval=top_buy; city_ufa_areas=; _PricesInPharm_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTMzZDQ3YzViY2MzNzAwYmM0ZmZjOTc3MzgwZDk1MjI2BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUFhU0dvMzNjaEcvakR2RHNKd1hmZk5LRjVtUVA1Wm93TUZONkhDVXZFd2M9BjsARg%3D%3D--70c37d55aa8b796c1f51688b4c2c5717077e456a; pharm_type=pharm; city=ufa; text=; isbliz=0; _ym_uid=15846297611018254784; _ym_d=1584629761; _ym_visorc_24215119=w; __utma=265944989.600108338.1584629761.1584629761.1584629761.1; __utmc=265944989; __utmz=265944989.1584629761.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; _ga=GA1.2.600108338.1584629761; _gid=GA1.2.514959953.1584629762; _gat_gtag_UA_48328690_1=1; test=1; tmr_lvid=5e4d4971d4bf4b3c37daf6071cf1239e; tmr_lvidTS=1584629763296; top100_id=t1.4469532.967003071.1584629763362; last_visit=1584611763367::1584629763367; _ym_isad=2; tmr_detect=0%7C1584629769572; f=1; tmr_reqNum=3; __utmb=265944989.2.10.1584629761'}
	url = 'https://cenyvaptekah.ru/ufa/antibiotiki'
	link_pool(get_html(url))
	#get_basket(cookie)
	toc = time.time()
	print(toc - tic)


