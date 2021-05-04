from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import ssl
import os
import sys
import os.path
try:
	_create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
	pass
else:
	ssl._create_default_hhtps_context = _create_unverified_https_context
#setup^

#gets page content and returns it
def get_page_content(url):
	try:
		html_response_text = urlopen(url).read()
		page_content = html_response_text.decode('utf-8')
		return page_content
	except Exception as e:
		return None

#cleans title
def clean_title(title):
	invalid_characters = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
	for c in invalid_characters:
		title=title.replace(c,'')
	return title

#gets all urls in current page
def get_urls(soup):
	links = soup.find_all('a')
	for link in links:
		if link not in crawled_urls:
			urls.append(link.get('href'))
	return urls

#check if url valid
def is_url_valid(url):
	if url is None:
		return False
	if re.search('#', url):
		return False
	if re.search('.jpg', url):
		return False
	if url == '/wiki/MoMA':
		return False
	match=re.search('^/wiki/',url)
	if match:
		return True
	else:
		return False

#change relative url to full url
def reformat_url(url):
	match=re.search('^/wiki/',url)
	if match:
		return "https://en.wikipedia.org"+url
	else:
		return url

#saves a page to text document
def save(text, path):
	f = open(path,'w', encoding = 'utf-8', errors = 'ignore')
	f.write(text)
	f.close()
#function definitions^

#reads and makes a list form the terms file
t = open("terms.txt", "r")
terms = []
for line in t:
	terms.append(line)
t.close()

#reads and makes a list form the seed urls file
u = open("seed_urls.txt", "r")
urls = []
for line in u:
	urls.append(line.lower())
u.close()

crawled_urls = []

def crawler(place):
	print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
	print('pages crawled: ' + str(place))
	print('checking:' + str(urls[place]))
	if is_url_valid(urls[place]):
		#parses page
		soup = BeautifulSoup(get_page_content(reformat_url(urls[place])),'html.parser')
		#extracts text
		page_text = soup.get_text().lower()
		#checks if url content matches terms
		term_match = 0
		for term in terms:
			if re.search(term, page_text, re.I):
				term_match += 1
			if term_match >= 2:
				get_urls(soup)
				file_path = os.path.join('savedPages', clean_title(soup.title.string) + '.html')
				if os.path.isfile(file_path):
					print("SKIPED")
					print("SKIPED")
					print("SKIPED")
					break
				else:
					crawled_urls.append(reformat_url(urls[place]))
					save(page_text, file_path)
					print('match #: ' + str(len(crawled_urls)))
				#file_path = os.path.join('savedPages', clean_title(soup.title.string) + '.html')
				#save(page_text, file_path)
				#print(file_path)
				break
	if len(crawled_urls) < 500:
		crawler(place+1)
	else:
		print('done parsing')

sys.setrecursionlimit(10**6)
crawler(0)

#saves crawled url to text document
f = open("crawled_urls.txt","w")
i = 1
print('saving started')
for url in crawled_urls:
	print('files saved: ' + str(i))
	f.write(str(i) + url + '\n')
	i += 1
f.close()
print('done saving')
