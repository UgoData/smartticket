# coding: utf-8

# ------ IMPORTS -----
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


class LoadCleanData:

    def __init__(self):
        self.data = []

# ------LOAD DATA -------
    @staticmethod
    def load_classes():
        """ Loading the Classes data """
        return pd.read_csv("../data/Classes.csv", encoding="latin-1", delimiter=";")

    @staticmethod
    def load_open_food_facts():
        """ Loading the Open Food Facts data """
        return pd.read_csv("../data/OpenFoodFacts_v2.csv", encoding="latin-1", delimiter=";")

    @staticmethod
    def load_open_beauty_facts():
        """ Loading the Open Beauty Facts data """
        return pd.read_csv("../data/fr.openbeautyfacts.org.products.csv", encoding="latin-1", sep='\t')

    # ------ DISCOVER DATA -------
    @staticmethod
    def shape_df(df):
        """ Shape of a dataframe"""
        print "Number of rows :", df.shape[0]
        print "Number of columns :", df.shape[1]

    @staticmethod
    def only_fr_data_from_open_ff(df):
        """ Select only the data of open food fact where country is France"""
        df["countries_fr"].fillna("", inplace=True)
        return df[df["countries_fr"].str.contains('France')]

    @staticmethod
    def add_merge_columns(df, col_list):
        """ Merge description columns"""
        df["product_name"].fillna("", inplace=True)
        df.loc[:, "merge_col"] = df.loc[:, "product_name"]
        for col in col_list:
            df[col].fillna("", inplace=True)
            df.loc[:, "merge_col"] = df.loc[:, "merge_col"] + " " + df.loc[:, col]

    @staticmethod
    def select_col_beauty_fact(df):
        """ select only important columns and only French products """
        df_temp = df[[
            "url", "product_name", "generic_name", "quantity",
            "brands_tags", "categories_fr", "stores", "countries_fr",
            "main_category_fr", "image_url"
        ]]
        df_temp = df_temp.loc[(df_temp["countries_fr"].str.contains('France')) & ~df_temp["product_name"].isnull()]
        # Clean empty columns
        col_with_na = [
            'generic_name', 'quantity', 'brands_tags', 'categories_fr',
            'stores', 'main_category_fr', 'image_url'
        ]
        for col in col_with_na:
            df_temp[col].fillna('', inplace=True)
        return df_temp

    # ------ PROCESSING -------
    def load_clean_data(self):
        """ Load and clean the data for Food and Beauty"""
        df_open_ff_raw = self.load_open_food_facts()
        df_open_ff = self.only_fr_data_from_open_ff(df_open_ff_raw)
        col_to_add_to_product_name = ["generic_name", "brands_tags"]
        self.add_merge_columns(df_open_ff, col_to_add_to_product_name)
        df_open_bf = self.select_col_beauty_fact(self.load_open_beauty_facts())
        self.add_merge_columns(df_open_bf, col_to_add_to_product_name)
        return df_open_ff, df_open_bf

    # ------ PRINT -------
    def print_outputs(self):
        df_classes = self.load_classes()
        df_open_ff, df_open_bf = self.load_clean_data()

        print "-"*50
        self.shape_df(df_open_ff)
        self.shape_df(df_open_bf)
        print "-"*50
        print df_classes
        print "-"*50
        print df_open_ff.columns
        print "-"*50
        print df_open_ff[["product_name", "generic_name", "merge_col", "cat_purchease"]].head()
        print "-"*50
        print "Number of distinct Stores :", len(df_open_ff["stores"].unique())
        print "Number of distinct Brands :", len(df_open_ff["brands_tags"].unique())
        print "-"*50
        print df_open_ff.cat_purchease.unique()
        print "-"*50
        for i in df_open_bf.columns:
            print i
        print df_open_bf.head()
        # print only_fr_data_from_open_ff(df_open_ff)["countries_fr"].value_counts()

# LoadCleanData().print_outputs()
