from numpy import array
import pickle
import warnings
import praw
from praw.models import MoreComments
import utils
import Secrets 


warnings.filterwarnings("ignore")
reddit = praw.Reddit(client_id=Secrets.cid, \
                     client_secret=Secrets.clientSec, \
                     user_agent='streamba_demo', \
                     username='streamba_demo', \
                     password=Secrets.redditPass)


cv = pickle.load(open(".\\Modelling\\cv.pkl", 'rb'))
model=pickle.load(open(".\\Modelling\\model.pkl",'rb'))


def postAnalysis(link):
    print("Performing post analysis for")
    print(link)
    print("\n")
    l=[]
    submission = reddit.submission(url=link)
    for comment in submission.comments.list():
        if isinstance(comment, MoreComments):
            continue
        elif len(l)>1000:
            continue
        l.append(utils.cleanText(comment.body))
    f=model.predict(cv.transform(l))
    a=(f==1).sum()
    b=(f==0).sum()
    if a>b:
        print("Result:Majority Positive \n")
    else:
        print("Result:Majority Negative \n")

meirl = reddit.subreddit('meirl')
subs=meirl.hot(limit=10)
for sub in subs:
    postAnalysis("https://www.reddit.com/"+sub.permalink)


