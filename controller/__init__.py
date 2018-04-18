import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import datetime
import schedule
import time

client = MongoClient('mongodb://admin:240992@ds147659.mlab.com:47659/news_digger')
database = client.news_digger
news = database.news


def get_g1_news():
    print 'Getting G1 news...'
    g1 = requests.get('http://g1.globo.com/')
    g1_html = g1.content
    soup = BeautifulSoup(g1_html, 'lxml')
    for post in soup.findAll('div', attrs={'class': 'feed-post-body'}):
        post_text = post.find('div', attrs={'class': 'feed-text-wrapper'})
        link = post_text.find('a')['href']
        resume = post_text.find('p').text
        subject = post_text.find('span', attrs={'class': 'feed-post-metadata-section'}).text
        new = {'link': link, 'resume': resume, 'subject': subject, 'created_at': datetime.datetime.utcnow()}
        if news.find({'link': link}).count() == 0 and subject != ' Agenda do dia ':
            news.insert_one(new)
    print 'G1 news updated'


schedule.every(10).seconds.do(get_g1_news)

while 1:
    schedule.run_pending()
    time.sleep(1)

