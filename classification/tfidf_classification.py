# coding: utf-8

# ------ IMPORTS -----
import cPickle
import warnings

import numpy as np
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
        vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5)
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

    def get_features_importance(self, model, X, tfidf_dict):
        importances = model.feature_importances_
        std = np.std([tree.feature_importances_ for tree in model.estimators_],
                     axis=0)
        indices = np.argsort(importances)[::-1]

        # Print the feature ranking
        print("Feature ranking:")

        for f in range(X.shape[1]):
            print("%d. feature %s (%f)" % (
            f + 1, tfidf_dict.keys()[tfidf_dict.values().index(indices[f])], importances[indices[f]]))

    def save_pickles(self, X_df, y):
        self.pickle_tfidf(self.tfidf_learning(X_df))
        self.pickle_rf(self.rf_learning(X_df, y, self.tfidf_learning(X_df)))

