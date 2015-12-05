#!/usr/bin/python
# -*- coding: utf8 -*-

import socket, string, time, ssl
import urllib.request, urllib.parse, urllib.error, re
import sys
import json
import requests
import argparse

network = 'irc.freenode.net'  ##last run,  wouldnt connect to abjects:9999
nick = 'nottly'
chan = ''
port = 7000

socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

searchterm = '0'  ###seems to stick at this value and not redefine in while loop
chanid = ''
page = ''
reverse = ''
class termcolors:
    """Asign some cheap color output for the shell."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[31m'
    YELLOW = '\033[33m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def do_search():
    searches = requests.get("http://ixirc.com/api/?q=%s&cid=%s&pn=%s" % (
        searchterm, chanid, page)).json()
    jsondata = json.loads(str(searches).replace("'", '"'))
    jsons = jsondata['results']
    return jsons

def print_search():
    for item in reversed(do_search()):
        title = item['name']
        packn = item['n']
        botn = item['uname']
        chan = item['cname']
        netw = item['naddr']
        size = item['szf']
        print(termcolors.RED + title + termcolors.GREEN + " from", chan,
              termcolors.BLUE + "on", netw + termcolors.ENDC)
        print(termcolors.RED + size + termcolors.YELLOW + " /msg",
              botn, "xdcc send", packn, termcolors.ENDC)
        print("---------------------------------------------")
    print(searchterm)
def print_pageinfo():
    for item in do_search():
        results = item['c']
        pagecount = item['pc']
        print(termcolors.RED + results + termcolors.GREEN + " results",
              termcolors.BLUE + "on total of ", pagecount + termcolors.ENDC)
        print("---------------------------------------------")

def main(network, nick, chan, port):
	socket.connect((network,port))
	irc = ssl.wrap_socket(socket)
	irc.send(bytes('NICK %s\r\n' % nick, "UTF-8"))
	print(irc.recv(4096))
	irc.send(bytes('USER %s %s %s :My bot\r\n' % (nick,nick,nick), "UTF-8"))
	print(irc.recv(4096))
	irc.send(bytes('JOIN #%s\r\n' % chan, "UTF-8"))
	print(irc.recv(4096))

	while True:
		data = irc.recv(4096)
		print(data)
		user_in = input(":")
		if user_in.find("!s") != -1:
			user_in = user_in[3:]
			searchterm = user_in  ##this isnt redefining for use in print_search 
			try:
				print_search()   ## results show but needs searchterm to work to be specific
			except KeyError:
				print("No Result Found")
		print(user_in)
		data = data.decode("UTF-8")
		if data.find("PING") != -1:
			irc.send(bytes('PONG '+data.split()[1]+'\r\n', "UTF-8"))
		if user_in.find('!q') != -1:
			irc.send(bytes('QUIT\r\n', "UTF-8"))
			exit()
		if user_in.find('!d') != -1:   ##to check for xfer
			bot_name = 'Dragonkeeper'
			pack_number = '1'
			#user_in = user_in[3:]   ## for option select  !d 1  will show as 1
			irc.send(bytes('PRIVMSG ' +  bot_name + ' :xdcc send ' + pack_number + '\r\n', "UTF-8"))
if __name__=='__main__':
    main(network, nick, chan, port)
