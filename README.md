# demoStreamba
A demonstration repository for Streamba Application

## Description
This code is designed to take in a post to a reddit post, collect all of the comments to that post. We then use a pre trained machine learning model to predict whether the sentiment of that comment is 'positive' or 'negative'. We count up these results for the post, printing the positive and negative totals to the screen, as well as the overall majority. The results of this are sent to an SQL server hosted on AWS.

The training data for the machine learning model was based on https://www.kaggle.com/kazanova/sentiment140. A dataset of twitter posts, the intention of this twitter data was to detect depression in social media. My tool could be used to aid in moderation. It would also be interesting to measure and track the negativity of reddit communties.

## Running the code
The python scripts are intended to be run from the command line. 
