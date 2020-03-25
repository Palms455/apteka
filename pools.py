import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import json



def get_html(url):
	user_agent = { 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Mobile Safari/537.36'}
	r = requests.get(url, headers = user_agent)
	return r.text


def link_pool(url):
	html = get_html(url)
	link_goods = set()
	group1 = set()
	soup = BeautifulSoup(html, 'lxml')
	groups = soup.find_all('div', {'class': 'span4 mb-10'})
	for item in groups:
		links = 'https://cenyvaptekah.ru' + item.find('a').get('href')
		group1.add(links)
	with Pool(4) as p:
		results = p.map(make_all, group1)
	for i in results:
		link_goods = link_goods.union(i)
	return link_goods

		
def make_all(url):
	html = get_html(url)
	return get_data(html)

def get_data(html):
	links = set()
	soup = BeautifulSoup(html, 'lxml')
	link_goods = soup.find_all('a', class_='nodecor')
	for i in link_goods:
		#print(i)
		if '0.00 руб.' not in i.find('span', class_='price_grid').text:
			links.add(('https://cenyvaptekah.ru' + i.get('href')))
	return links


def offers(html):
	add_params = {}
	goods = []
	print('in offers')
	#response = requests.get(link)
	#print(response.status_code)
	data = BeautifulSoup(html, 'lxml')
	basket = data.select('.row-fluid>.buy-btn-div>a.btn.btn-info')
	for item in basket:
		dat = item.get('onclick')[28:-1].split(',')
		add_params['good_id'] = dat[0]
		add_params['pharm_id'] = dat[1]
		add_params['offer_id'] = dat[2]
		#add_params['price'] = dat[3]
		add_params['is_ad'] = dat[4]
		goods.append(add_params)
	return goods 
