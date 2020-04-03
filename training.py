from pandas import read_csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

from numpy import array
import pickle
import warnings
warnings.filterwarnings("ignore")
import utils

stopwords = set(utils.stopwords.words('english') + list(utils.punctuation) + ['AT_USER','URL'])
dataset_path=".\\TrainingData\\training.1600000.processed.noemoticon.csv"

def saveDataset(filepath):
    colNames = ["target", "ids", "date", "flag", "user", "text"]
    df = read_csv(dataset_path, encoding="ISO-8859-1", names=colNames)
    df=df.drop(["ids","flag","date","user"], axis = 1)
    df.target=df.target.replace(4,1)
    return df

def trainModel():
    print("Running trainModel:")
    print("Loading data")
    df= saveDataset(dataset_path)                 
    df["text"]=df["text"].apply(utils.cleanText)
    tweets=df['text'].tolist()
    
    print("Vectorising")
    cv=CountVectorizer(max_df=0.85,stop_words=stopwords,max_features=10000)
    word_count_vector=cv.fit_transform(tweets)
    
    print("Fitting model")
    model = MultinomialNB()
    model.fit(word_count_vector,array(df["target"]))
    
    print("Saving model")
    pickle.dump(cv,open(".\\Modelling\\cv.pkl", 'wb'))
    pickle.dump(model,open(".\\Modelling\\model.pkl", 'wb'))

def main():
    trainModel()
        
if __name__ == "__main__":
    main()
        
