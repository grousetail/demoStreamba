# demoStreamba
A demonstration repository for Streamba Application

## Description
This code is designed to take in a link to a reddit post and collect all of the comments to that post. We then use a pre trained machine learning model to predict whether the sentiment of that comment is 'positive' or 'negative'. We count up these results for the post, printing the positive and negative totals to the screen, as well as the overall majority. The results of this are sent to an SQL server hosted on AWS.

The training data for the machine learning model was based on https://www.kaggle.com/kazanova/sentiment140. A dataset of twitter posts, the intention of this twitter data was to detect depression in social media. My tool could be used to aid in moderation. It would also be interesting to measure and track the negativity of reddit communties.

## Running the code
The python scripts are intended to be run from the command line. 

### training.py
Requires the training data to be available. It is not include in the git repo due to size but it can be found at. https://www.kaggle.com/kazanova/sentiment140
this data should be run in the TrainingData folder

### predict.py
This requires the Secrets.py included in the same location. This will be provided upon request.
 
To be run with a path to a text file containing the reddit posts that need to be searched. An example set of posts is provided in exmp.txt the syntax is then.

**predict.py exmp.txt**

### Python environment
The code was written in python 3.6. The neccesary packages to run this code can be found at req.txt and can be loaded using:

**pip install -r req.txt**
