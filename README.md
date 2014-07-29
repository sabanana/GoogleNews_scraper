GoogleNews_scraper
==================

simply scrape everyday news from news.google.com


1. To run the program, type "python scrape_GoogleNews.py".

2. You need to change line 19 on GoogleNewsScraper.py ---- " self.basePath = "/Users/daisypang/Documents/my_python27/GoogleNews" " to the root directory of the GoogleNews folder on your computer. 

3. This program imports "Chardet" module to detect the encoding charset of the web page. You may need to install "Chardet" to run the program. Tell me if it is difficult to do so on the grid. I'll modify the program.

4. I've add some error-control function to this program to deal with the annoying "UnicodeEncodingError" problem and the "403 Forbidden" error throughs by the web site. And I've run this program on my computer continuously for more than 3 hours. Hopefully this program should be able to run continuously on the grid for days. But I still can't guarantee that no exception would occur. So it would be very nice of you if you forward me the email the grid sends you so that I can fix the program and restart it on time ;)

5. This scraper collects news from the following Topics on news.google.com:
Top Story, World, U.S, Business, Technology, Entertainment, Sports, Science, Health, Spotlight. (Not including Detroit MI local news).

What We Can Do Next

1. It would be very helpful to debug the program if it outputs a logging.txt to keep records its crawling status. "logging" module of python enables such function but I haven't fully figure out how to use this module so far.

2. Somehow this crawler runs slowly on collecting every news while the updating of news on the Google News web site is fast. It would crawl faster and collect much more news if it runs on multithread (or parallel computing ) to crawl news of different Topics on the same time.
