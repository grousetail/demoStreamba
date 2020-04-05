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

### server.py
This requires the Secrets.py included in the same location. This will be provided upon request.

This code is used to run a flask server on the localhost:5000. If you are running this for the first time you will need to run 

`set FLASK_APP=server.py` - All code was run on windows

To run the flask server the syntax is:

`flask run`

This will listen for POST requests, along with data like {'url': posturl} and use the model to predict whether the overall sentiment is positve,negative or neutral.

On the server side it will also record how many positive and negative comments there were and log this in an SQL database

### req.py
This python contains an example POST request to be sent to the server. To run this, with the flask server running, the syntax is:

`python req.py`

### Python environment
The code was written in python 3.6. The neccesary packages to run this code can be found at requirements.txt and can be loaded using:

`pip install -r requirements.txt`
 
### SQL Database
The SQL database is hosted on AWS and the main table that we will be inserting into is `redditTable`

## Shortcomings
For data that is not particulary expressive or very short, it is basically a coin toss for prediction. For example:

"This is the follow up I needed"

"Ya know, if you had a jewel on a staff and a large 3D map on the ground, you might be able to find the Ark of the Covenant."

"I am a bot, and this action was performed automatically. Please [contact the moderators of this subreddit](/message/compose/?to=/r/politics) if you have any questions or concerns."

Would all be classified as negative.
