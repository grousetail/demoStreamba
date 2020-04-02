from numpy import array
import pickle
import warnings
import praw
from praw.models import MoreComments
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from string import punctuation 
import re

warnings.filterwarnings("ignore")
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

a='https://www.reddit.com/r/AskReddit/comments/ftk07k/whats_a_really_awkward_situation_that_everyone/?utm_source=share&utm_medium=web2x'


def postAnalysis(link):
    print("Performing post analysis for")
    print(link)
    l=[]
    submission = reddit.submission(url=link)
    for comment in submission.comments.list():
        if isinstance(comment, MoreComments):
            continue
        elif len(l)>1000:
            continue
        l.append(cleanText(comment.body))
    f=model.predict_proba(cv.transform(l))
    print(f)
    print((f==1).sum())
    print((f==0).sum())

meirl = reddit.subreddit('rarepuppers')
subs=meirl.hot(limit=10)
for sub in subs:
    postAnalysis("https://www.reddit.com/"+sub.permalink)


