#coding=utf-8
import urllib
import urllib2
import os
import sys
import re
import io
import time
import codecs
import chardet
import logging
from bs4 import BeautifulSoup


class GoogleNewsScraper:

	def __init__(self):
		self.baseURL = "https://news.google.com"
		self.basePath = "/Users/daisypang/Documents/my_python27/GoogleNews"
		self.Topics = {}

		#
		# Create logger to output log to console and write in file "GnewsScraper.log"
		#
		logger = logging.getLogger('GnewsScraperLogger')
		logger.setLevel(logging.DEBUG)

		fh = logging.FileHandler('GnewsScraper.log')
		fh.setLevel(logging.INFO)

		ch = logging.StreamHandler()
		ch.setLevel(logging.DEBUG)

		formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
		fh.setFormatter(formatter)
		ch.setFormatter(formatter)

		logger.addHandler(fh)
		logger.addHandler(ch)



	def getTopics(self):
		"""Form URLs of Topics and save them to self.channels"""
		print "*** Preparing URLs of Topics...\n"

		Topics_Short = {}
		Topics_Short['World'] = 'w'
		Topics_Short['US'] = 'n'
		Topics_Short['Business'] = 'b'
		Topics_Short['Technology'] = 'tc'
		Topics_Short['Entertainment'] = 'e'
		Topics_Short['Sport'] = 's'
		Topics_Short['Science'] = 'snc'
		Topics_Short['Health'] = 'm'
		Topics_Short['Spotlight'] = 'ir'

		self.Topics['TopStory'] = self.baseURL

		for TopicKey in Topics_Short.keys():
			self.Topics[TopicKey] = self.baseURL + '/news/section?pz=1&cf=all&topic=' + Topics_Short[TopicKey]



	def getEncoding(self,html_doc,soup):
		"""Get encoding from header of the website.
		Return the string of Encoding 'encod'"""
		
		#soup = BeautifulSoup(html_doc)

		if soup.meta == None:
			print "\n", html_doc

		encod = soup.meta.get('charset')
		if encod == None:
			encod = soup.meta.get('content-type')
			if encod == None:
				content = soup.meta.get('content')
				if content != None:
					match = re.search('charset=(.*)',content)
				else:
					match = None
				if match:
					encod = match.group(1)
				else:
					dic_of_possible_encodings = chardet.detect(html_doc)
					encod = dic_of_possible_encodings['encoding']

		print "encoding_in_header = ", encod
		return encod



	def getRTC(self, TopicName):
		"""Get links to 'See Realtime Coverage' of each Topic page,
		return list -- RTCs[]"""
		print " ---Getting RTCs of Topic: ", TopicName

		TopicURL = self.Topics[TopicName]
		RTCs = []
		flagSuccess = 0
		tryTimes = 0

		while flagSuccess == 0 and tryTimes <= 8:
			try:
				opener = urllib2.build_opener()
				opener.addheaders = [('User-agent', 'Mozilla/5.0')]
				ufile = opener.open(TopicURL)
				html_doc = ufile.read()

				re_RTC = r'<a class="goog-inline-block jfk-button jfk-button-action esc-fullcoverage-button" href="[^>]*>See realtime coverage</a>'
				URLs_RTC = re.findall(re_RTC, html_doc)

				for URL in URLs_RTC:
					soup = BeautifulSoup(URL)
					RTCs.append(self.baseURL + soup.a['href'])

				print "  -- ", len(RTCs), " RTC links Found !!!"

				flagSuccess = 1
				tryTimes += 1

			except IOError:
				print "  -- Encounter IOError when opening URL: ", TopicURL
				print "  -- tryTimes: ", tryTimes
				print "  -- Wait a minute......"
				time.sleep(6)
				tryTimes += 1

		return RTCs



	def getSAA(self, RTCs):
		"""Get links to 'See all articles' in each 'rtc' pages,
		return list -- SAAs[]"""
		print " ---Getting SAAs..."

		SAAs = []
		if len(RTCs) == 0:
			print "  -- Error!!! The RTCs[] is empty !!!"
		else:
			for RTC in RTCs:
				flagSuccess = 0
				tryTimes = 0

				while flagSuccess == 0 and tryTimes <= 8:
					try:
						opener = urllib2.build_opener()
						opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
						ufile = opener.open(RTC)
						html_doc = ufile.read()

						#print "RTC = ", RTC
						re_SAA = r'<a [^>]*>See all[^>]*articles[^>]*</a>'
						if re.search(re_SAA, html_doc) != None:
							find_SAA = re.search(re_SAA, html_doc).group()
							soup = BeautifulSoup(find_SAA)
							SAA = self.baseURL + soup.a['href']
							SAAs.append(SAA)
						else:
							SAAs.append(None)

						flagSuccess = 1
						tryTimes += 1

					except IOError:
						print "  -- Encounter IOError when opening RTC_URL: ", RTC
						print "  -- tryTimes: ", tryTimes
						print "  -- Wait a minute......"
						time.sleep(6)
						tryTimes += 1

		return SAAs



	def getArtcURLs(self, SAA_URL, pageNum, URLs_article):
		"""Recursively get links to every article in every page of 'See all articles' and save them in
		list URLs_article"""
		print "   -- Getting article links from SAA_URL: ", SAA_URL
		print "   -- Page: ", pageNum

		if SAA_URL == None:
			print "   -- Error!!! SAA_URL is None!!!"
		else:

			flagSuccess = 0
			tryTimes = 0
			while flagSuccess ==0 and tryTimes<=8:
				try:
					opener = urllib2.build_opener()
					opener.addheaders = [('User-agent', 'Mozilla/5.0')]
					ufile = opener.open(SAA_URL)
					html_doc = ufile.read()

					flagSuccess = 1
					tryTimes += 1
				except IOError:
					print "   -- Encounter IOError when opening SAA_URL: ", SAA_URL
					print "   -- tryTimes: ", tryTimes
					print "   -- Wait a minute......"
					time.sleep(6)
					tryTimes += 1

			if flagSuccess == 1:
					soup = BeautifulSoup(html_doc)
					list_h2 = soup.find_all('h2')

					print "   -- Number of Articles: ", len(list_h2)
					for i in range(len(list_h2)):
						h2 = list_h2[i]
						soup_h2 = BeautifulSoup(str(h2))
						if soup_h2.a != None:

							if soup_h2.a.string != None:
								article_title1 = unicode(soup_h2.a.string)
							else:
								span = unicode(soup_h2.span)
								article_title1 = re.search(r'<span class="titletext">([^<]*)<b>[^<]*</b></span>', span).group(1)

							article_title = article_title1.replace('?',' ').replace('/','-').replace('\\','-').replace('"',' ').replace(':','-').encode('utf-8', 'replace')
							article_link = unicode(soup_h2.a['href'])
							URLs_article[article_title] = article_link

					flag_next = soup.find("td", {"class" : "next"} )
					if flag_next != None:
						soup_flagNext = BeautifulSoup(unicode(flag_next))
						URL_next = soup_flagNext.a['href']
						self.getArtcURLs(self.baseURL + URL_next, pageNum+1, URLs_article)
					else:
						return
					



	def ScrapeArticle(self, articleURL, articleTitle, savePath):
		"""Scraping single article from articleURL and save the .txt file under dir
		savePath if the article does not exist"""
		print "# Scraping: ", articleTitle, " ..."
		print "#      URL: ", articleURL

		Title_List = os.listdir(savePath)
		f_article_name = articleTitle + '.txt'

		if f_article_name not in Title_List:
		
			flagSuccess = 0
			tryTimes = 0

			while flagSuccess==0 and tryTimes <= 5:
				try:
					hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.1) Gecko/20100101 Firefox/10.0.1'}
					req = urllib2.Request(articleURL, headers=hdr)
					html_doc = urllib2.urlopen(req).read()

					tryTimes += 1
					flagSuccess = 1
					#print "tryTimes: ",tryTimes

				except IOError:
					print " - Failed!!! Encounter IOError."
					print " - tryTimes: ", tryTimes
					print " - Wait a minute......"
					time.sleep(6)
					tryTimes += 1

			if flagSuccess == 1:
					soup = BeautifulSoup(html_doc)
					if soup.meta != None:
						article = []
						article.append(articleTitle + '\n\n')
						article.append(articleURL + '\n\n')

						encoding_in_header = self.getEncoding(html_doc,soup)

						p_list = soup.find_all('p')
						for p_line in p_list:
							article.append(p_line.text + '\n')

						f_article = codecs.open(savePath + '/' + f_article_name,'w', encoding=encoding_in_header)
						for str_line in article:

							#strline2 = str_line.decode(encoding_in_header,'ignore')         # Important!!!
							try:
								f_article.write(str_line)
							except UnicodeEncodeError:
								print " - UnicodeEncodeError: ", encoding_in_header
								f_article.write(" <UnicodeEncodeError: "+encoding_in_header+"> ")
							except UnicodeDecodeError:
								print " - UnicodeDecodeError: ", encoding_in_header
								f_article.write(" <UnicodeDecodeError: "+encoding_in_header+"> ")
							#f_article.close()

						print " - COLLECTED ^_^"
					else:
						print " - No Avaliable Content!!!"
				

		else:
			print " - REPEATED!!!"



	def ScrapeTopic(self, TopicName):
		"""Scraping all articles in the Topic.
		Calling methods: getRTC(), getSAA(), getArtcURLs(), ScrapeArticle()"""
		print "*** Scraping Topic: ", TopicName, " ..."

		TopicPath = self.basePath + '/' + TopicName
		if not os.path.exists(TopicPath):
			os.mkdir(TopicPath)

		RTCs = self.getRTC(TopicName)
		SAAs = self.getSAA(RTCs)
		for SAA_URL in SAAs:
			URLs_article = {}
			self.getArtcURLs(SAA_URL, 1, URLs_article)
			for article_title in URLs_article.keys():
				self.ScrapeArticle(URLs_article[article_title], article_title, TopicPath)

		
