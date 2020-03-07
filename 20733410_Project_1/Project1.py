import requests
import json
from datetime import datetime
from datetime import date
from operator import itemgetter
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import movie_reviews
import random


response = requests.get("https://api.nytimes.com/svc/movies/v2//reviews/{type}.json?&api-key=zsj6S6woq0N2XiwkstPiAik9it6jwZki") #gets the newset 20 reviews

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=0)
    print(text)

print(response.status_code)
#jprint(response.json())


text = response.json()['results']

#entryt format = [display_title, opening_date, date_updated, byline, summary_short] # display_title, opening_date, date_updated, byline, summary_short
my_list = [] 

my_reviews = []

###collecting data from API and storing into arrray
for d in text:
    
    entry = []
    x1 = d['display_title']
    entry.append(x1)

    x2 = d['opening_date']
    
    if(x2!=None and x2!='0000-00-00'):
        Time_opening_date1 = datetime.strptime(x2, '%Y-%m-%d')
        entry.append(date(Time_opening_date1.year, Time_opening_date1.month, Time_opening_date1.day))
    else:
        Time_opening_date1 = datetime.strptime('1999-01-01', '%Y-%m-%d')
        entry.append(date(Time_opening_date1.year, Time_opening_date1.month, Time_opening_date1.day))
     

    x3 = d['date_updated']
    Time_date_updated = datetime.strptime(x3, '%Y-%m-%d %H:%M:%S')
    entry.append(Time_date_updated)
    

    x4 = d['byline']
    entry.append(x4)

    x5 = d['summary_short']
    entry.append(x5)

    x6 = d['link']['url']
    entry.append(x6)

    ###addinf array to list 
    my_list.append(entry)

###sorting list via 1st and 2nd elemnets (date release, date update)
sorted_list = sorted(my_list, key=itemgetter(1,2),reverse = True)


index = ["movie title", "Opening date", "Last mod", "author", "summary", "URL"] 

### printing of 15 reviews
for v in range(15):
    print(str(v+1) +": ")
    for i in range(5): 
        
        if i == 1:

            if sorted_list[v][1].year == datetime.strptime('1999', '%Y').year :
                print("null")
            else:
                print(sorted_list[v][i])
        else:
            print(sorted_list[v][i])
        #   print(index[i] +": "+ my_list[i][v])

    ### get the full review
    html_content = requests.get(sorted_list[v][5]) #gets the newset 20 reviews ?&api-key=zsj6S6woq0N2XiwkstPiAik9it6jwZki

    #print(html_content.status_code)

    soup = BeautifulSoup(html_content.content, 'html.parser')

    rev = ""
    for hit in soup.findAll(attrs={'class' : 'css-exrw3m evys1bk0'}):
        rev = rev + hit.text
    ### 
    my_reviews.append(rev)
    print(rev)

    ###is review positive or negative
    documents = [(list(movie_reviews.words(fileid)), category)
              for category in movie_reviews.categories()
              for fileid in movie_reviews.fileids(category)]
    random.shuffle(documents)

    for hit in soup.findAll(attrs={'class' : 'css-exrw3m evys1bk0'}):
        rev = rev + hit.text
    rev_word_list = rev.split()

    all_words = nltk.FreqDist(w.lower() for w in rev_word_list)
    word_features = list(all_words)[:2000]

    def document_features(document):
        document_words = set(document)
        features = {}
        for word in word_features:
            features['contains({})'.format(word)] = (word in document_words)
        return features

    featuresets = [(document_features(d), c) for (d,c) in documents]
    train_set, test_set = featuresets[100:], featuresets[:100]
    classifier = nltk.NaiveBayesClassifier.train(train_set)

    classifier.show_most_informative_features(5)

        

    print("___________________________________________")
    print()

      
    ### end of single review with all details

### all reviews printed
