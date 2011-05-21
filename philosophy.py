#!/bin/python

import urllib2
import urllib
import sys
from BeautifulSoup import BeautifulSoup

def strip_brackets(string):
	"""
	remove brackets from a string
	leave brackets between "<a></a>" tags in place
	hihi, this is like an automata
	"""
	string = "" + str(string)
    	#print "input: ",string
    	d = 0
    	k = 0
    	out = ''
    	for i in string:
    		#check for tag when not in parantheses mode
		if d < 1:
			if i == '>':
				k-=1
				
			if i =="<":
				k +=  1
			
		#check for parentheses
		if k < 1:
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
		
    	#print "output: ",out
    	return out

class PhilosophyGame():
	"""
	This class folows a given, or in other case random wikipedia article
	and folows it's trace to the philosophy page
	each time following the first link in the content, skipping links between parentheses
	based on http://imgur.com/mqlKD
	depends on beatifulsoup

	still has some utf8 problems
	"""
	def __init__(self,prefix="http://en.wikipedia.org",userAgent='Mozilla/5.0'):
		self.opener = urllib2.build_opener()
		self.opener.addheaders = [('User-agent', userAgent)]
		self.prefix = prefix

	

	def trace(self,article):
		"""
		trace the first link in each article, that's not between parentheses
		"""
		print article
		#TODO: check for loops?
		#and maybe fix them? :p
		#currently loops between Phonetic_transcription and International_Phonetic_Alphabet
		#TODO: use dynamic computing (caching of results)
		resource = self.opener.open(article)
		data = resource.read()
		resource.close()
		soup = BeautifulSoup(data)
		for i in soup.find('div',id="bodyContent").findAll({'ul' : True, 'p' : True},recursive=False):
			#find first link here that isn't in parenthesis
			i = BeautifulSoup(strip_brackets(i))
			#print i
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
	
				if next == "Philosophy":
					print "You have arrived"
					return
				else:
				
					if not nexturl.startswith("http://"):
						nexturl = self.prefix + nexturl
					self.trace(nexturl)
					return

if __name__ == "__main__":
	game = PhilosophyGame()
	if len(sys.argv) == 1 :
		game.trace("http://en.wikipedia.org/wiki/Special:Random")
	else:
		for i in sys.argv[1:]:
			game.trace("http://en.wikipedia.org/wiki/" + i)
