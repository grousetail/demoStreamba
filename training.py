from pandas import read_csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

from numpy import array
import pickle
import warnings
warnings.filterwarnings("ignore")
import utils


stopwords = set(utils.stopwords.words('english') + list(utils.punctuation) + ['AT_USER','URL'])

# Training data not included in git as its too large
dataset_path = ".\\TrainingData\\training.1600000.processed.noemoticon.csv"


# Description: Loads training data into df, removing irrelevant coloumns and 
#              converting the target variables into something more workable.
# 
# Variables
#   filepath (string) - Filepath to training data

def saveDataset(filepath):
    colNames = ["target", "ids", "date", "flag", "user", "text"]
    df = read_csv(dataset_path, encoding="ISO-8859-1", names=colNames)
    df = df.drop(["ids","flag","date","user"], axis = 1)
    df.target = df.target.replace(4,1)
    return df

# Description: Takes in our training data and models using a Naive Bayes model.
#              saves as pickle files to be used by our predictors.


def trainModel():
    print("Running trainModel:")
    print("Loading data")
    df = saveDataset(dataset_path)                 
    df["text"] = df["text"].apply(utils.cleanText)
    tweets = df['text'].tolist()
    
    print("Vectorising")
    
    # Data must be converted to matrix format to be readable by our model. 
    # Keeping our features low prevents the model from becoming overcomplicated
    cv = CountVectorizer(max_df=0.85,stop_words=stopwords,max_features=10000)
    word_count_vector = cv.fit_transform(tweets) 
    
    print("Fitting model")
    model = LogisticRegression(C=1.) # Logistic regression provided a slightly 
    #                                  better auc score compared to NB 
    #                                 (0.878>0.877). I tried to keep models simple
    
    # model = MultinomialNB()
    
    model.fit(word_count_vector,array(df["target"]))
    
    print("Saving model")
    pickle.dump(cv,open(".\\Modelling\\cv.pkl", 'wb'))
    pickle.dump(model,open(".\\Modelling\\model.pkl", 'wb'))

def main():
    trainModel()
        
if __name__ == "__main__":
    main()
        
