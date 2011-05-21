#!/bin/python

import urllib2
import urllib
import sys
from BeautifulSoup import BeautifulSoup



"""
This scripts folows a given, or in other case random wikipedia article
and folows it's trace to the philosophy page
each time following the first link in the content, skipping links between parentheses
based on http://imgur.com/mqlKD
depends on beatifulsoup

still has some utf8 problems
"""

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
prefix = "http://en.wikipedia.org"

def strip_brackets(string):
	"""
	remove brackets from a string
	leave brackets between "<a></a>" tags in place
	hihi, this is like an automata
	"""
	print "input",string
	string = "" + str(string)
    	d = 0
    	k = 0
    	out = ''
    	for i in string:
    		#check for <a tag when not in parantheses mode
        	if d < 1:
			if k==3:
				if i ==">":
					k=0
				else:
					k=2
					
			if k == 2 and i == 'a':
				k = 3
				
			if k == 1:
				if i == 'a':
					k=2
				else:
					k = 0
					
			if k==0 and i =="<":
				k =  1
				
        	#check for parentheses
        	if k < 2:
			if i == '(':
		    		d += 1
	
			if d > 0:
		    		out += ' '
			else:
		    		out += i

			if i == ')' :
		    		d -= 1
		else:
			out +=i
		    	
	print "output",out
    	return out

def trace(article):
	"""
	trace the first link in each article, that's not between parentheses
	"""
	print article
	#TODO: check for loops?
	#and maybe fix them? :p
	#currently loops between Phonetic_transcription and International_Phonetic_Alphabet
	resource = opener.open(article)
	data = resource.read()
	resource.close()
	soup = BeautifulSoup(data)
	for i in soup.find('div',id="bodyContent").findAll('p',recursive=False):
		#find first link here that isn't in parenthesis
		i = BeautifulSoup(strip_brackets(i))
		#print i
		#fails on greek?? sgmllib why you no like characters in position 157-166 ?
		#f.ex on architecture
		for j in i.findAll('a'):
			k = 0
			for val,att in j.attrs:
				if val =="href":
					nexturl =att
				if val =="title":
					next = att 
					k=1
			if k==0: #citations or something, no title, skipp
				continue
	
			next = urllib.quote(next)
			#urllib.quote  fails on http://en.wikipedia.org/wiki/Old_Norman ?? (unicode)
			if next == "Philosophy":
				print "You have arrived"
				return
			else:
				
				if not nexturl.startswith("http://"):
					nexturl = prefix + nexturl
				trace(nexturl)
				return
	
		#TODO:
		#if you have arrived here there were no plain links in this paragraph,
		#probably they were all enumerated, allow links in ul li tags.
		#f.ex http://en.wikipedia.org/wiki/Group and http://en.wikipedia.org/wiki/Components


	
	
if len(sys.argv) == 1 :
	trace("http://en.wikipedia.org/wiki/Special:Random")
else:
	for i in sys.argv[1:]:
		trace("http://en.wikipedia.org/wiki/" + i)
