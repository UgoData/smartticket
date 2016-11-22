# coding: utf-8

# ------ IMPORTS -----
import cPickle
import warnings

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

from loadAndCleanData import LoadCleanData
from processTextData import ProcessText

warnings.filterwarnings("ignore")

print "INTO TFIDF CLASSIF"

p = ProcessText()
l = LoadCleanData()


class Classification:
    def __init__(self):
        self

    @staticmethod
    def load_data():
        """
        :return: X and y for classification
        """
        # Load all dataset
        df = l.load_and_concat()
        X_df = p.clean_text_data(df)['merge_final']
        y = df['cat_purchease']
        return X_df, y

    def tfidf_learning(self, X_df):
        vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, min_df=0.005, ngram_range=(1, 2))
        return vectorizer.fit(X_df)

    def rf_learning(self, X_df, y, tf_idf):
        input_vect = tf_idf.transform(X_df)
        rf = RandomForestClassifier(n_estimators=10, random_state=123, min_samples_leaf=1)
        return rf.fit(input_vect, y)

    def pickle_tfidf(self, tf_idf):
        with open("../models/dumpTfIdf.pkl.gz", "wb") as file1:
            cPickle.dump(tf_idf, file1)
        print ("TF - IDF saved")

    def pickle_rf(self, rf):
        with open("../models/dumpRf.pkl.gz", "wb") as file1:
            cPickle.dump(rf, file1)
        print ("Random Forest saved")

    def tfidf_rf_classif_apply(self, tf_idf_load_from_pickle, rf_load_from_pickle, list_input):
        tf_idf_trans = tf_idf_load_from_pickle.transform(list_input)
        return rf_load_from_pickle.predict(tf_idf_trans)

    def save_pickles(self, X_df, y):
        self.pickle_tfidf(self.tfidf_learning(X_df))
        self.pickle_rf(self.rf_learning(X_df, y, self.tfidf_learning(X_df)))

# c = Classification(['pain maxi burger', 'HAR. VERT XF'])
# X_df, y = c.load_data()

# c.save_pickles(X_df, y)

# print c.tfidf_rf_classif_apply(tf_idf_load_from_pickle, rf_load_from_pickle)
