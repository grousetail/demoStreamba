from numpy import array
import pickle
import warnings
import praw
from praw.models import MoreComments
import utils
import Secrets 
import pyodbc 
from datetime import datetime
import sys


warnings.filterwarnings("ignore")
reddit = praw.Reddit(client_id=Secrets.cid, \
                     client_secret=Secrets.clientSec, \
                     user_agent='streamba_demo', \
                     username='streamba_demo', \
                     password=Secrets.redditPass)


cv = pickle.load(open(".\\Modelling\\cv.pkl", 'rb'))
model=pickle.load(open(".\\Modelling\\model.pkl",'rb'))
con = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                     'SERVER='+Secrets.server+';UID='
                     +Secrets.username+
                     ';PWD='+
                     Secrets.redditPass+';Initial Catalog=StreamDemo')
cur = con.cursor()


def insertTab(link,pos,neg,result):
    cur.execute('INSERT INTO StreamDemo.dbo.redditTable'
                '(link,positive_comments,negative_comments,overall_majority)'
                'VALUES (\''+link+"\',"+str(pos)+","+str(neg)+",\'"+result+"\');")
    con.commit()
    

def postAnalysis(link):
    print("Performing post analysis for")
    print(link)
    print("\n")
    print(datetime.now())
    l=[]
    submission = reddit.submission(url=link)
    for comment in submission.comments.list():
        if isinstance(comment, MoreComments):
            continue
        elif len(l)>1000:
            continue
        l.append(utils.cleanText(comment.body))
    
    if (len(l))<1:
        insertTab(link,0,0,"None")
        print("No comments found")
        return
    
    preds=model.predict(cv.transform(l))
    pos=(preds==1).sum()
    neg=(preds==0).sum()
    if pos>neg:
        insertTab(link,0,0,"Positive")
        print("Result:Majority Positive \n")
    elif pos<neg:
        insertTab(link,0,0,"Negative")
        
        print("Result:Majority Negative \n")
    else:
        insertTab(link,pos,neg,"None")
 
def main():
    meirl = reddit.subreddit('AskReddit')
    subs=meirl.hot(limit=15)
    for sub in subs:
        postAnalysis("https://www.reddit.com/"+sub.permalink)
        
if __name__ == "__main__":
    main()
        
        
