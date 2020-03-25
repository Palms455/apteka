from pools import link_pool, offers
from time import time
from bs4 import BeautifulSoup
import requests
import csv
from random import choice
from multiprocessing import Pool
from sel_mode import Bot

def get_proxy():
	html = requests.get('https://free-proxy-list.net/').text
	proxies = []
	soup = BeautifulSoup(html, 'lxml')
	trs = soup.find('table', id= 'proxylisttable').find('tbody').find_all('tr')[:12]
	for tr in trs:
		tds = tr.find_all('td')
		adress = tds[0].text.strip()
		port = tds[1].text.strip()
		schema = 'https' if 'yes' in tds[6].text.strip() else 'http'
		proxy = {'schema': schema, 'adress': adress + ':' + port}
		proxies.append(proxy)
	return choice(proxies)

def get_proxy_html(url):
	#proxies = {'https': 'ipaddress: 5000'}
	print('getting proxy')
	p = get_proxy() #{'schema': '' , 'adress': ''}
	proxy = {p['schema']: p['adress'],
			p['schema']: p['adress'],
			p['schema']: p['adress'],
			p['schema']: p['adress'],
			p['schema']: p['adress'],} # можно указать несколько прокси
	print('proxy')
	try:
		r = requests.get(url, proxies=proxy, timeout=5 )
		print(r.status_code)
	except:
		print('bad request. retrying')
		return get_proxy_html(url)
	
	return r.text

def pool_offers(link_set):
	with Pool(4) as p:
		result = p.map(Bot, link_set)
	print(result)


def make_offers(url):
	html = get_proxy_html(url)
	return offers(html)




if __name__ == '__main__':
	tic = time()
	cookie = {'cookie': '__cfduid=d62fe2da8ffeb7073f3e8ba82c4b17c561584629759; tval=top_buy; city_ufa_areas=; _PricesInPharm_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTMzZDQ3YzViY2MzNzAwYmM0ZmZjOTc3MzgwZDk1MjI2BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUFhU0dvMzNjaEcvakR2RHNKd1hmZk5LRjVtUVA1Wm93TUZONkhDVXZFd2M9BjsARg%3D%3D--70c37d55aa8b796c1f51688b4c2c5717077e456a; pharm_type=pharm; city=ufa; text=; isbliz=0; _ym_uid=15846297611018254784; _ym_d=1584629761; _ym_visorc_24215119=w; __utma=265944989.600108338.1584629761.1584629761.1584629761.1; __utmc=265944989; __utmz=265944989.1584629761.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; _ga=GA1.2.600108338.1584629761; _gid=GA1.2.514959953.1584629762; _gat_gtag_UA_48328690_1=1; test=1; tmr_lvid=5e4d4971d4bf4b3c37daf6071cf1239e; tmr_lvidTS=1584629763296; top100_id=t1.4469532.967003071.1584629763362; last_visit=1584611763367::1584629763367; _ym_isad=2; tmr_detect=0%7C1584629769572; f=1; tmr_reqNum=3; __utmb=265944989.2.10.1584629761'}
	url = 'https://cenyvaptekah.ru/ufa/antibiotiki'
	link_set = link_pool(url)
	print('got link_set')
	print(link_set)
	pool_offers(link_set)
	toc = time()
	print(toc - tic)