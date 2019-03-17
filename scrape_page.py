import requests
import urllib2
# import time
# from bs4 import BeautifulSoup

url = 'https://www.sports-reference.com/cbb/schools/san-diego-state/2013.html'
req = urllib2.Request(url)
response = urllib2.urlopen(req)

print (response.read())
# soup = BeautifulSoup(response.text, "html.parser")

