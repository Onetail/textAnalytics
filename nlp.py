from pykafka import KafkaClient
import jieba
from gensim import corpora, models, similarities
import pandas as pd
import sys

jieba.set_dictionary('dict.txt.big')
stop_word = ['【', '】', '「','」', '《', '》','（','）', '。', '，','、','：','“','”','_','？','!','〝','〞','…','；','『','』','｛','｝','＃','＆','＊','．','‧','-','+','=','—','–']
stop_word += ['和','的','是','了','也']

def tokenization(data):
    result = []
    for word in jieba.cut(data, cut_all=False):
        if word not in stop_word:
            result.append(word)
    return result

def getNews(subject):
    client = KafkaClient(hosts="127.0.0.1:9092")
    topic = client.topics[subject]
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,consumer_timeout_ms=5000)
    
    data = [] 
    for message in consumer:
        if message is not None:
            print(message.offset, (message.value).decode('utf-8'))
            data.append((message.value).decode('utf-8'))
    return data



def analysis(subject):
    data = getNews(subject)

    #create corpus
    corpus=[]
    for i in data:
        corpus.append(tokenization(i))

    #build TF-IDF Model
    dictionary = corpora.Dictionary(corpus)
    doc_vectors = [dictionary.doc2bow(text) for text in corpus]
    tfidf = models.TfidfModel(doc_vectors)
    tfidf_vectors = tfidf[doc_vectors] 
    print(dictionary)

    def articleSim(article):
        query = tokenization(article)
        query_bow = dictionary.doc2bow(query)
        index = similarities.MatrixSimilarity(tfidf_vectors)
        sims = index[query_bow]
        return sims

    result =[]
    for idx,val in enumerate(data):
        row = []
        row.append('Id_'+str(idx+1))
        for i in articleSim(val):
            row.append(str(i))
        result.append(row)

    return result


if __name__ == '__main__':
    subject = ""
    if(sys.argv[1]=='politics'):
        subject = 'politics'
    elif(sys.argv[1]=='entertainment'):
        subject = 'entertainment'
    else:
        print("input topic")

    result = analysis(bytes(subject,'utf-8'))
    pd.DataFrame(result).to_csv(subject+'.csv',index=False,header=False)
