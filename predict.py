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
reddit = praw.Reddit(client_id = Secrets.cid, 
                     client_secret = Secrets.clientSec, 
                     user_agent = 'streamba_demo', 
                     username = 'streamba_demo', 
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
#   results (string) - The overall majority result for the classification i.e.
#                      if there are more positive than negative we say positive
#                      or none if it's a tie.

def insert_tab(link, pos, neg, result):
    cur.execute('INSERT INTO StreamDemo.dbo.redditTable'
                '(link,positive_comments,negative_comments,overall_majority)'
                'VALUES (\'' + link + "\'," + str(pos) + "," + str(neg) + ",\'" + result + "\');")
    con.commit()
    

# Description: Using our model, classifies values into positive or negative
#              also prints result to screen.
# 
# Variables
#   link (string) - Link to Reddit post.

def post_analysis(link):
    print("Performing post analysis for")
    print(link)
    l = []
    submission = reddit.submission(url=link)
    for comment in submission.comments.list():
        if isinstance(comment, MoreComments):
            continue
        
        # For large comment threads the extra comments don't provide much 
        # additional information and can slow down prediction dramatically
        elif len(l) > 1000:
            continue
        l.append(utils.clean_text(comment.body))
    
    # If the thread contains no comments 
    if (len(l)) < 1:
        insert_tab(link, 0, 0, "None")
        print("No comments found")
        return
    
    preds = model.predict(cv.transform(l))
    pos = (preds==1).sum()
    neg = (preds==0).sum()
    
    print("Positive comments: " + str(pos))
    
    print("Negative Comments: " + str(neg))
    
    if pos > neg:
        insert_tab(link, pos, neg, "Positive")
        print("Result:Majority Positive \n")
    
    elif pos < neg:
        insert_tab(link, pos, neg, "Negative")
        print("Result:Majority Negative \n")
    
    else:
        insert_tab(link,pos,neg,"None")
 
def main():
    arg = sys.argv[1]
    links = open(arg, "r")
    for link in links:
        post_analysis(link)
    
if __name__ == "__main__":
    main()
        

        
