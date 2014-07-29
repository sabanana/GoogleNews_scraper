#coding=utf-8
from GoogleNewsScraper import GoogleNewsScraper
import sys
import os
import time


def main():

	ROUND = 1
	Gnews = GoogleNewsScraper()
	Gnews.getTopics()
	while(True):
		print "< ROUND > ", ROUND, "\n"
		for Topic in Gnews.Topics.keys():
			Gnews.ScrapeTopic(Topic)

		print "\n...ROUND ", ROUND, " completed !"
		print "...Sleep for 5 minutes...ZZZzzzzzzz..."
		time.sleep(120)
		ROUND += 1




if __name__ == '__main__':
	main()
