from seleniumwire import webdriver
from ip_read import get_proxy_ip

f = get_proxy_ip('ip_selenium.txt')

wire_options = {
	'proxy':{
		'https': f,  #get_proxy_ip('ip_selenium.txt'),
		'http': f,
		}
	}
#options = webdriver.ChromeOptions()
#options.add_argument('headless')
driver= webdriver.Chrome(seleniumwire_options=wire_options)
driver.get('https://cenyvaptekah.ru/ufa/amoxicillin_kaps_500mg_n16')