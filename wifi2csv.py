#!/usr/bin/python3
#coder: kodo no kami

import os
import sys
import re
import time

argo = 0
argopen = 0
argwpa = 0
argwpa2 = 0
argoutro = 0
filtro = ""
argbssid = ""
interface = "wlan0"
argohelp = 0 

argc = len(sys.argv[1::])
argcont = 1	
while(argcont <= argc):
	if(sys.argv[argcont] == "--open"):
		argopen = 1
		argo = 1
	elif(sys.argv[argcont] == "--wpa"):
		argwpa = 1
		argo = 1
	elif(sys.argv[argcont] == "--wpa2"):
		argwpa2 = 1
		argo = 1
	elif(sys.argv[argcont] == "--bssid"):
		argbssid = sys.argv[argcont + 1]
		argo = 1
		argcont += 1
	elif(sys.argv[argcont] == "--iface"):
		interface = sys.argv[argcont + 1]
		argcont += 1
	elif(sys.argv[argcont] == "--help"):
		argohelp = 1
	else:
		argo = 1
		filtro = sys.argv[argcont]

	argcont += 1


if(argohelp):
	print("[--- WIFI2CSV ---]\ncoder: kodo no kami\n\n" \
	"sintax: python script.py <param> ...\n\n" \
	"--bssid <BSSID>: especifica o bssid\n" \
	"--iface <INTERFACE>: espeficica a interface wlan\n" \
	"--open: lista apenas as redes abertas\n" \
	"--wpa: lista apenas as redes wpa\n" \
	"--wpa2: lista apenas as redes wpa2\n" \
	"<FILTRO>: filtra SSID usando regex\n" \
	"\nex:\n python script.py\n python script.py --iface wlan0 --open\n python script.py escritorio\n"
	)
	
	exit(0)
	
comando = "sudo iwlist {} scan".format(interface)

cmd = os.popen(comando,"r")

mac = ""
essid = ""
sinal = ""
frequ = ""
canal = ""
wpa1_s = ""
wpa1_cipher = ""
wpa2_s = ""
wpa2_cipher = ""
encrypt = ""

primeiro = 0
iie1 = 0
iie2 = 0

todos = []

for c in cmd:
	texto = c
	ma = re.search("Cell \d+ .*?Address: (\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)",texto)
	if(ma):
		if(primeiro == 0):
			primeiro = 1
		else:
			exibir = 0
			if(argo == 0):			
				exibir = 1
			if((wpa1_s) and (argwpa) and (not wpa2_s)):
				exibir = 1
			if((wpa2_s) and (argwpa2) and (not wpa1_s)):
				exibir = 1
			if((argopen) and (encrypt == "off")):
				exibir = 1
			if((wpa1_s) and (argwpa) and  (argwpa2) and (wpa2_s)):
				exibir = 1
			if(argbssid == mac):
				exibir = 1
			if(filtro):
				fil = re.search(filtro,essid,re.I)
				if(fil):
					exibir = 1
		
			if(exibir):
				todos.append("{},{},{},{},{},{},{},{}".format(mac,essid,sinal,frequ,canal,cripto_t,cipher_t,encrypt))
		
		mac = ""
		essid = ""
		sinal = ""
		frequ = ""
		canal = ""
		wpa1_s = ""
		wpa2_s = ""
		wpa1_cipher = ""
		wpa2_cipher = ""
		iee1 = 0
		iee2 = 0

		mac = ma[1]
	else:
		essi = re.search("ESSID:\"(.*)\"",texto)
		if(essi):
			essid = essi[1]
			essid = re.sub(",",".",essid)
			
		sina = re.search("Signal level=(.*) dBm",texto)
		if(sina):
			sinal = sina[1]

		freq = re.search("Frequency:(.*?) GHz .Channel (\d+)\D",texto)
		if(freq):
			frequ = freq[1]
			canal = freq[2]
			re.sub(",",".",canal)

		wpa1 = re.search("WPA Version 1",texto)
		
		if(wpa1):
			wpa1_s = "WPA"
			iie1 = 1
			iie2 = 0
		
		wpa2 = re.search("WPA2 Version 1",texto)
		if(wpa2):
			wpa2_s = "WPA2"
			iie1 = 0
			iie2 = 1

		enc = re.search("Encryption key:(\w+)",texto)
		if(enc):
			encrypt = enc[1]
			
		ciphe = re.search("Group Cipher : (\w+)",texto)
		if(ciphe):
			cipher  = ciphe[1]
			if(iie1 == 1):
				wpa1_cipher = ciphe[1]
			if(iie2 == 1):
				wpa2_cipher = ciphe[1]
		
		cripto_t = wpa1_s + "-" + wpa2_s
		cripto_t = re.sub("^\-","",cripto_t)
		cripto_t = re.sub("\-$","",cripto_t)
			
		cipher_t = wpa1_cipher + "-" + wpa2_cipher
		cipher_t = re.sub("^\-","",cipher_t)
		cipher_t = re.sub("\-$","",cipher_t)

exibir = 0
if(argo == 0):			
	exibir = 1
if((wpa1_s) and (argwpa) and (not wpa2_s)):
	exibir = 1
if((wpa2_s) and (argwpa2) and (not wpa1_s)):
	exibir = 1
if((argopen) and (encrypt == "off")):
	exibir = 1
if((wpa1_s) and (argwpa) and  (argwpa2) and (wpa2_s)):
	exibir = 1
if(argbssid == mac):
	exibir = 1
if(filtro):
	fil = re.search(filtro,essid,re.I)
	if(fil):
		exibir = 1
	
if(exibir):
	todos.append("{},{},{},{},{},{},{},{}".format(mac,essid,sinal,frequ,canal,cripto_t,cipher_t,encrypt))

for t in todos:
	print(t)
