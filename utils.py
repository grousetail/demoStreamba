
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from string import punctuation 
import re

# Description: Simplifies text data by stemming and removing 
#              users and urls, as well as unnecessary white space. 
# 
# Variables
#   text (string) - Any string data to be cleansed


def clean_text(text):
    text=text.lower()
    text = text.split()
    text = [PorterStemmer().stem(word=x) for x in text]
    text = " ".join(text)
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', text)
    text = re.sub('@[^\s]+', 'AT_USER', text)
    text = re.sub(r'#([^\s]+)', r'\1', text) 
    text = re.sub('[\s]+', ' ', text)
    return text