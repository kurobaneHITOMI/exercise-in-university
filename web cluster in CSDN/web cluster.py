################################################################
################################################################
import requests
from bs4 import BeautifulSoup
import bs4
import os
os.chdir("D:\\课程\\2018\\数据挖掘\\3")
import re
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
#web url list
url_list = []
for i in range(1,11):
    url_list.append('http://blog.csdn.net/?ref=toolbar_logo&page='+str(i))          
#article url        
blog_urls = []
for url in url_list:
    html = requests.get(url, headers=headers)
    html.encoding = html.apparent_encoding
    soup = BeautifulSoup(html.text, 'html.parser')
    for h2 in soup.find_all('h2'):
            blog_url = (h2('a')[0]['href'])
            blog_urls.append(blog_url)
#load acticles
blog_data = {}
i = 1
for url in blog_urls:
    blog_html = requests.get(url, headers=headers)
    blog_html.encoding = blog_html.apparent_encoding
    soup = BeautifulSoup(blog_html.text, 'html.parser')
    blog_data[i] = soup.select('div')[0].text
    blog_data[i] = re.sub('[\n]', '', blog_data[i])
    i += 1

#get the title
def get_title(urldata):
    
    title = []
    for url in urldata:
        blog_html = requests.get(url, headers=headers)
        blog_html.encoding = blog_html.apparent_encoding
        soup = BeautifulSoup(blog_html.text, 'html.parser') 
        title.append(re.sub('\n','',soup.select('h1')[0].text).replace(' ', ''))
        
    return(title)

title = get_title(blog_urls)

################################################################
################################################################
#pretreatment
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer 
import jieba
import gensim
from gensim import corpora,similarities, models
import glob
from sklearn.decomposition import PCA





#delete punctuation
i = 1
for url in blog_data:
    blog_data[i] = re.sub(u'[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。，。？、~@#￥%……&*（）]','',blog_data[i])
    i +=1

#delete stop words
stopwords = open('stopwords.txt').read()
stopwords = stopwords.split()
def DeleteStopWords(data):  

    wordList = []  
    cutWords = jieba.cut(re.sub('\s','',data))  
    for item in cutWords:  
        if item not in stopwords:
            wordList.append(item)  

    return wordList  

i = 1
for url in blog_data:
    blog_data[i] = DeleteStopWords(blog_data[i])
    i +=1


#tf-idf analysis
i = 1
line = ''
corpus = []
for url in blog_data:
    texts = blog_data[i]
    for word in texts:
        line += word
        line += ' ' 
    corpus.append(line)
    
    
    
def TFIDF(corp):
    
    corp = corpus
    #a[i][j] means frequence of word j in article i 
    vectorizer = CountVectorizer()  
    # tf-idf weight
    transformer = TfidfTransformer()    
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corp))    
    # get tf-idf matrix
    weight = tfidf.toarray()  
    
    return weight  

blog_data_matrix = TFIDF(corpus)


#PCA
blog_data_set = PCA(n_components=20).fit_transform(blog_data_matrix)



################################################################
################################################################
#cluster
from sklearn.cluster import KMeans
k = 3
clusterer = KMeans(n_clusters=k, init='k-means++')
y = clusterer.fit_predict(blog_data_set)

blog = []
y = list(y)

for i in range(209):
    blog.append({'url':blog_urls[i+1] , 'title':title[i] , 'label':y[i]})






    
