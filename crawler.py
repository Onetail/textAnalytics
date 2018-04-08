import requests 
from bs4 import BeautifulSoup
import sys
from pykafka import KafkaClient

client = KafkaClient(hosts="120.79.72.101:9092") #ali cloud server
topic = None
host = "https://tw.news.yahoo.com/"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
headers = { 'User-Agent' : user_agent }

def getContent(url):
    res = requests.get(url,headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,"html.parser")
    article =""
    for i in soup.select('article'):
        article+=i.get_text()
    return article

def getDiv(url):
    res = requests.get(url,headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,"html.parser")

    for i in soup.select('div[id="YDC-Stream"] > ul > li'):
        if(i.div.get('class')[0]!='controller'):
            data = {} 
            title = i.div.div.h3.a.get_text()
            link = url+i.div.div.h3.a.get('href')
            print(title,link)
            content = getContent(link).strip()
            if(content!=''):
                with topic.get_sync_producer() as producer:
                    producer.produce(bytes(content,'utf-8'))
            else:
                print('null data')
if __name__ == '__main__':
    if(sys.argv[1]=='politics'):
        topic = client.topics[b'politics']
        getDiv(host+'politics')
    elif(sys.argv[1]=='entertainment'):
        topic = client.topics[b'entertainment']
        getDiv(host+'entertainment')
    else:
        print("input topic")
    

