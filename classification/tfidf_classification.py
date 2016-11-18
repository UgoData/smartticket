# coding: utf-8

# ------ IMPORTS -----
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from processTextData import ProcessText
from loadAndCleanData import LoadCleanData
import warnings
warnings.filterwarnings("ignore")


class TfIdf:

    def __init__(self):
        self.data = []

    def tf_idf(self, df):
        vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5)
        return vectorizer.fit(df['merge_final'])

p = ProcessText()
l = LoadCleanData()
df = p.clean_text_data(l.load_and_concat())
print "Size of df :", df.shape
print "test"
tfidf_trained = TfIdf().tf_idf(df)
X_df = tfidf_trained.transform(df['merge_final'])
print "Sike x_df :", X_df.shape

Y_df = l.load_and_concat()['cat_purchease']
print "Sike y_df :", Y_df.shape

class Classification:
    def __init__(self):
        self.data = []

    def rfClassif(self, X, y):
        """ Classification Random Forest avec input tf_idf"""
        clf = RandomForestClassifier(n_estimators=10)
        return clf.fit(X, y)

    def rfPredict(self, clf, tfidf, receipt_line):
        """ Prediction of the category of receipt_line"""
        receipt_tfidf = tfidf.transform(receipt_line)
        return clf.predict(receipt_tfidf)

clf = Classification().rfClassif(X_df, Y_df)
print Classification().rfPredict(clf, tfidf_trained, ['pain maxi burger','HAR. VERT XF'])

