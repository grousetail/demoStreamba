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

# Warnings arise when models are run on different versions of python 3 but 
# cause no operational effects.
warnings.filterwarnings("ignore")

# Connecting to Reddit client.
reddit = praw.Reddit(client_id = Secrets.cid, \
                     client_secret = Secrets.clientSec, \
                     user_agent = 'streamba_demo', \
                     username = 'streamba_demo', \
                     password = Secrets.redditPass)


# Loading Models
cv = pickle.load(open(".\\Modelling\\cv.pkl", 'rb'))
model = pickle.load(open(".\\Modelling\\model.pkl",'rb'))

# Connecting to AWS MSSQL server
con = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                     'SERVER=' + Secrets.server + ';UID='
                     + Secrets.username + ';PWD=' +
                     Secrets.redditPass + ';Initial Catalog=StreamDemo')
cur = con.cursor()

# Description: Inserts new values into the SQL database
# 
# Variables
#   link (string) - link used in Reddit lookup.
#   pos (int) - The number of positive classified comments.
#   neg (int) - The number of negatively classified comments.
#   results (string) - The over all majority result for the classification i.e.
#                      if there are more positve than negative we  say positive
#                      or none if its a tie.

def insertTab(link,pos,neg,result):
    cur.execute('INSERT INTO StreamDemo.dbo.redditTable'
                '(link,positive_comments,negative_comments,overall_majority)'
                'VALUES (\''+link+"\'," + str(pos) + ","+str(neg) + ",\'" + result + "\');")
    con.commit()
    

# Description: Using our model, classifys values into positive or negative
#              also prints result to screen.
# 
# Variables
#   link (string) - Link to Reddit post.

def postAnalysis(link):
    print("Performing post analysis for")
    print(link)
    l = []
    submission = reddit.submission(url=link)
    for comment in submission.comments.list():
        if isinstance(comment, MoreComments):
            continue
        
        # For large comment threads the extra comments dont provide much 
        # additional information and can slow down prediction dramaticaly
        elif len(l)>1000:
            continue
        l.append(utils.cleanText(comment.body))
    
    # If the thread contains no comments 
    if (len(l))<1:
        insertTab(link,0,0,"None")
        print("No comments found")
        return
    
    preds=model.predict(cv.transform(l))
    pos = (preds==1).sum()
    neg = (preds==0).sum()
    
    print("Positive comments: "+str(pos))
    
    print("Negative Comments: "+str(neg))
    
    if pos>neg:
        insertTab(link,0,0,"Positive")
        print("Result:Majority Positive \n")
    
    elif pos<neg:
        insertTab(link,0,0,"Negative")
        print("Result:Majority Negative \n")
    
    else:
        insertTab(link,pos,neg,"None")
 
def main():
    arg=(sys.argv)[1]
    links = open(arg, "r")
    for link in links:
        postAnalysis(link)
    
if __name__ == "__main__":
    main()
        

        
