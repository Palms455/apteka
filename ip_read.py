from random import choice
from login_pass import passw


@passw
def get_proxy_ip(folder):
	with open(folder, 'r') as f:
		reader = list(f.readlines())
		ip = [i.strip("\n")+':7165' for i in reader]
		return choice(ip)



