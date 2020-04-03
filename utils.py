
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from string import punctuation 
import re

# Description: Simplfys text data by stemming and cleaning weird sections. 
# 
# Variables
#   text (string) - Any string data to be cleansed


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