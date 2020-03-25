from seleniumwire import webdriver
import time
from bs4 import BeautifulSoup
import requests
import csv
from random import randint
import json
from random import choice

class Bot:
	def __init__(self, url):
		self.url = url
		#self.options = {
    	#'proxy': self.get_proxy_html('https://2ip.ru/')
		#}
		self.options = webdriver.ChromeOptions()
		#self.options.add_argument('headless')
		#self.driver= webdriver.Chrome(seleniumwire_options=self.options)
		self.driver = webdriver.Chrome(options = self.options)
		self.add_count = 0 # счетчик товаров в корзине()
		self.driver.implicitly_wait(5)
		self.navigate()


	'''
	def get_proxy(self):
		#парсит список прокси адресов
		html = requests.get('https://free-proxy-list.net/').text
		proxies = []
		soup = BeautifulSoup(html, 'lxml')
		trs = soup.find('table', id= 'proxylisttable').find('tbody').find_all('tr')[:12]
		for tr in trs:
			tds = tr.find_all('td')
			adress = tds[0].text.strip()
			port = tds[1].text.strip()
			schema = 'https' if 'yes' in tds[6].text.strip() else 'http'
			proxy = {'schema': schema, 'adress': schema + '://' + adress + ':' + port}
			proxies.append(proxy)
		return choice(proxies)

	def get_proxy_html(self, url):
		#функция тестирует прокси на предмет работоспособности и передает в selenium
		print('getting proxy')
		user_agent = { 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Mobile Safari/537.36'}
		p = self.get_proxy() #{'schema': '' , 'adress': ''}
		adress = p['adress'][(p['adress'].rfind('://')) + 3 :]
		proxy = {p['schema']: adress,}
		print(proxy) # можно указать несколько прокси
		try:
			r = requests.get(url, proxies=proxy, headers=user_agent, timeout=3 )
			print(r.status_code)
		except:
			print('bad request. retrying')
			return self.get_proxy_html(url)
		if r.status_code == 503 or r.status_code == 200:
			print('ok')
			return {p['schema']: p['adress']}
		else:
			self.get_proxy_html(url)
		'''


	def navigate(self):
		self.driver.get(self.url)
		try:
			self.driver.find_element_by_css_selector('.alert-first-usage__content a').click()
		except:
			pass
		self.add_basket()
		#self.driver.quit()
	

	def add_basket(self):
		#добавляет товары в корзину
		try:
			next_page = self.driver.find_element_by_css_selector('div.dataTables_paginate.paging_bootstrap.pagination ul :nth-child(5)')
			# проверка на наличие следующей страницы в таблице с товарами
		except:
			next_page = None
			self.add_action()
		if next_page:	
			while True:
				self.add_action()
				if 'disabled' not in next_page.get_attribute('class'):
					next_page.find_element_by_tag_name('a').click()
				else:
					self.in_basket()
					break
		return


	def add_action(self):
		# действие по добавлению товаров
		self.driver.execute_script("window.scrollTo(0, 0);")
		buttons = self.driver.find_elements_by_css_selector('.row-fluid>.buy-btn-div>a.btn.btn-info')
		for button in buttons:
			button.click()
			time.sleep(randint(2,5))
			self.add_count += 1
			if self.add_count >= 20:
				# сайт не позволяет добавлять более 22-24 товаров.
				self.in_basket(1) 
				self.add_count = 0
		return


	def remove_action(self):
		# очистка корзины товаров
		removals = self.driver.find_elements_by_css_selector('a.btn i.icon-remove')
		for remove in removals:
			remove.click
		return


	def in_basket(self, mode = None):
		# переход к корзине товаров 
		self.driver.execute_script("window.open()")
		self.driver.switch_to.window(self.driver.window_handles[1])
		self.driver.get("https://cenyvaptekah.ru/city/ufa/pharm/basket/index")
		time.sleep(5)
		self.get_basket()
		if mode:
			self.remove_action()
	
		self.driver.switch_to.window(self.driver.window_handles[0])
		return 
			

	def get_basket(self):
		#выдергивание со страницы нужной инфы
		adreses = self.driver.find_elements_by_css_selector('[data-bind="attr:{href: pharm_href}, text: pharm_name"]')
		good_table = self.driver.find_elements_by_css_selector('tbody#basketRowsBody')
		for item in range(len(good_table)):
			adres = adreses[item].text
			goods = good_table[item].find_elements_by_tag_name('tr')
			for good in goods:
				pharm_name = good.find_element_by_css_selector('a[data-bind="attr: {href: href}, text: pharm_good_name(), css:{qtyerrorpoz: is_rest_error , \'basket-no-row-for-pharm\': is_not_row_visible_for_pharm }"]').text
				pharm_rest = good.find_element_by_css_selector('span[data-bind="text: pharm_rest_text, css:{qtyerror: is_rest_error, \'basket-no-row-for-pharm-rest\': is_not_row_visible_for_pharm }"]').text
				pharm_price = good.find_element_by_css_selector('span[data-bind="text: pharm_price_text, css:{qtyerrorpoz: is_rest_error, \'basket-no-row-for-pharm\': is_not_row_visible_for_pharm }"]').text
				pharm = {'pharm_name': pharm_name,
						'pharm_adres': adres,
						'price': pharm_price,
						'quantity': pharm_rest,
						}
				self.write_csv(pharm)

		
	def write_csv(self, pharm):
		#запись в CSV файл
		with open('grm.csv', 'a',encoding='utf-8') as file:
			order = ['pharm_name', 'pharm_adres', 'price', 'quantity']
			writer = csv.DictWriter(file, fieldnames=order)
			print('write in to csv')
			writer.writerow(pharm)


