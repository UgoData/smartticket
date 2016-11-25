# -*- coding: utf-8 -*-
import cPickle as pickle

import pandas as pd

from googlePlaces import GoogleApi
from tfidf_classification import Classification

c = Classification()


def test_classification_via_apprentissage():
    #### Test classification via apprentissage
    X_df, y = c.load_data()

    vectorizer = c.tfidf_learning(X_df)

    model = c.rf_learning(X_df, y, vectorizer)

    print model.predict(vectorizer.transform(['CHOCO', 'TOURNESOL MOZZARELLA', 'CHAUSSON FRUIT'
                                                                               '6X XTREME3 P SENSI', 'Tomates Cerises',
                                              'poire'
                                                 , 'X72 LINGET EAU NET', 'Bianco, boisson aromatisée blanc']))

    vectorizer = c.tfidf_learning(X_df)
    vocab = vectorizer.vocabulary_
    idf = vectorizer.idf_
    dense = vectorizer.transform(X_df).todense()
    df_tiidf = pd.DataFrame(dense, columns=[x for (x, z) in sorted(vocab.items(), key=lambda (k, v): v)])
    df_tiidf['categories'] = y
    dict_res = {}
    for cat_name in df_tiidf['categories'].unique():
        print cat_name
        df_temp = df_tiidf[df_tiidf['categories'] == cat_name]
        list_col = []
        for col in df_temp.columns:
            if df_temp['col'].sum() > 0:
                list_col.append(col)
        dict_res[cat_name] = list_col
    print dict_res
    print dict(zip(vectorizer.get_feature_names(), idf))

    c.get_features_importance(model, vectorizer.transform(X_df), vocab)


def test_classification_via_pickle():
    #### Test CLassification

    # Load TF-IDF
    tf_idf_load_from_pickle = pickle.load(open("../models/dumpTfIdf.pkl", "rb"))
    # Load Random Forest
    rf_load_from_pickle = pickle.load(open("../models/dumpRf.pkl", "rb"))

    print c.tfidf_rf_classif_apply(tf_idf_load_from_pickle, rf_load_from_pickle, ['CHOCO', 'TOURNESOL MOZZARELLA'])


def test_google_api():
    #### Test Google API
    g = GoogleApi('churrasquera galo restaurant', '69 rue de dunkerque 75009')
    print "Result from Google API :", g.return_only_one_category(
        g.convert_googletypes_into_rmwtypes(g.get_place_type_from_google(g.get_place_infos())))


test_classification_via_apprentissage()
