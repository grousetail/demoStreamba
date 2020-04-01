from numpy import array
import pickle
import warnings
import praw

from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from string import punctuation 
import re

#warnings.filterwarnings("ignore")
reddit = praw.Reddit(client_id='bTewNJ5si7SyVw', \
                     client_secret='IyiNqH4dSbJvzvfvYqsxUewUNH4', \
                     user_agent='streamba_demo', \
                     username='streamba_demo', \
                     password='aa123456')

def cleanText(text):
    text=text.lower()
    text = text.split()
    text = [PorterStemmer().stem(word=x) for x in text]
    text=" ".join(text)
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', text)
    text = re.sub('@[^\s]+', 'AT_USER', text)
    text = re.sub(r'#([^\s]+)', r'\1', text) 
    text = re.sub('[\s]+', ' ', text)
    return text

cv = pickle.load(open(".\\Modelling\\cv.pkl", 'rb'))
model=pickle.load(open(".\\Modelling\\model.pkl",'rb'))

submission = reddit.submission(url='https://www.reddit.com/r/CasualUK/comments/fs85h6/isolation_day_12_two_women_mid_30s_no_children/')

l=[]
submission.comments.replace_more(limit=200)
for comment in submission.comments.list():
    l.append(comment.body)
    
print(cleanText(l[0]))