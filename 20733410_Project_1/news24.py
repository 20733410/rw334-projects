import requests
import json
from datetime import datetime
from datetime import date
from operator import itemgetter
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import movie_reviews
import random
from newspaper import Article 

html_content = requests.get("https://www.news24.com/") #gets the newset 20 reviews ?&api-key=zsj6S6woq0N2XiwkstPiAik9it6jwZki



soup = BeautifulSoup(html_content.content, 'html.parser')
URLs = [] #to store URLS in MOST READ TAB 

#gets all urls in most read TAB and stores them, 

for box in soup.findAll(attrs={'class' : 'grid_4'}):
    for tag in box.find_all(attrs={'id' : 'tab_read_data','class' : 'tab-wrapper'} ):
        for item in tag.find_all(attrs={'class' : 'bold'}): 
            for link in item.find_all('a'):   
                URLs.append(link.get('href'))

mv_url = URLs[0]

url_content = requests.get(mv_url) 
article = Article(mv_url)
article.download()
article.parse()
article.nlp()

soup2 = BeautifulSoup(url_content.content, 'html.parser')

title = ""
title_list = []

#gets headline
#title = soup2.find(attrs={'class' : 'article_header'})

'''for box in soup2.findAll('title'):
        title = title + box.text
        #title_list.append(box.text)
title_list = title.splitlines()

for pos in range(len(title_list)):
    if(title_list[pos]!=''):
        title = title_list[pos]
        break
'''

#gets text

text = ""

#works for specific fromat 
'''
for box in soup2.findAll(attrs={'id' : 'article-body'}):
    for box in box.findAll('p'):
        text = text + box.getText()'''

#gets all text not just article :(

'''for item in soup2.find_all('p'):
    text = text + item.text()
'''


#print(title)
#print(title_list)
#print(text)

#using article better :)
print(article.title)
print(article.text)
