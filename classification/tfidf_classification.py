# coding: utf-8

# ------ IMPORTS -----
import warnings

from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

from loadAndCleanData import LoadCleanData
from processTextData import ProcessText

warnings.filterwarnings("ignore")

p = ProcessText()
l = LoadCleanData()


class Classification:
    def __init__(self, input):
        self.input = input

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

    def rf_pipeline_classif(self, params_grid, num_folds=3):
        """
        :param df: Raw DataFrame
        :param params_grid: Grid of parameters
        :param num_folds: Number of folds for CV
        :return: fitted model / results of CV
        """
        X_df, y = self.load_data()
        vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, min_df=0.005, ngram_range=(1, 2))
        rf = RandomForestClassifier(n_estimators=10, random_state=123)
        pipe = Pipeline([('tfidf', vectorizer), ('rf', rf)])
        model = GridSearchCV(pipe, param_grid=params_grid, n_jobs=1, cv=num_folds, verbose=1, refit=True)

        return model.fit(X_df, y), model.cv_results_

    def rf_pipeline_classif_gridsearch(self):
        # Load all dataset
        df = l.load_and_concat()

        params_grid = {'tfidf__min_df': [0, 0.0005, 0.001],
                       'rf__min_samples_leaf': [1, 3, 5],
                       }

        (model, results) = Classification().rf_pipeline_classif(df, params_grid, num_folds=3)
        print results
        # Results have been saved into result_gridsearch.json
        # Best parameters are : tfidf__min_df=0.0005 and rf__min_samples_leaf=1

    def tfidf_learning(self, X_df):
        vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, min_df=0.005, ngram_range=(1, 2))
        return vectorizer.fit(X_df)

    def rf_learning(self, X_df, y, tf_idf):
        input_vect = tf_idf.transform(X_df)
        rf = RandomForestClassifier(n_estimators=10, random_state=123, min_samples_leaf=1)
        return rf.fit(input_vect, y)

    def pickle_tfidf(self, tf_idf):
        with open("../models/dumpTfIdf.pkl.gz", "wb") as file1:
            # cPickle.dump(model, file1)
            joblib.dump(tf_idf, file1)
            # pkl.dump(model, open( "testPickle.p", "wb" ) )
        print ("TF - IDF saved")

    def pickle_rf(self, rf):
        with open("../models/dumpRf.pkl.gz", "wb") as file1:
            # cPickle.dump(model, file1)
            joblib.dump(rf, file1)
            # pkl.dump(model, open( "testPickle.p", "wb" ) )
        print ("Random Forest saved")

    def tfidf_rf_classif_apply(self):
        # Load TF-IDF
        tf_idf = joblib.load(open("../models/dumpTfIdf.pkl.gz", "rb"))
        # Load Random Forest
        rf = joblib.load(open("../models/dumpRf.pkl.gz", "rb"))
        return rf.predict(tf_idf.transform(self.input))

    def save_pickles(self, X_df, y):
        self.pickle_tfidf(self.tfidf_learning(X_df))
        self.pickle_rf(self.rf_learning(X_df, y, self.tfidf_learning(X_df)))


c = Classification(['pain maxi burger', 'HAR. VERT XF'])
# X_df, y = c.load_data()

# c.save_pickles(X_df, y)

print c.tfidf_rf_classif_apply()
