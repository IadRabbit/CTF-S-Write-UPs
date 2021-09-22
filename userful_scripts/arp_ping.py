#!/usr/bin/python3

from scapy.config import Conf
from scapy.layers.l2 import Ether, ARP, srp

conf = Conf()

def get_vendor(mac):
	vendor = conf.manufdb._get_manuf(mac)

	return vendor

ans, unans = (
	srp(
		Ether(dst = "ff:ff:ff:ff:ff:ff")/
		ARP(pdst = "192.168.1.0/24"),
		timeout = 2,
		verbose = 0
	)
)

for answered in ans:
	ip = answered[1].psrc
	mac = answered[1].hwsrc
	vendor = get_vendor(mac)
	print(ip, mac, vendor)