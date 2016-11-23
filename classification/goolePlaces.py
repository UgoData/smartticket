# coding: utf-8

# ------ IMPORTS -----
import pandas as pd
import requests as r

KEY_GOOGLE = 'AIzaSyAd_AwyPpw6Coc591WWqI2duRUN1E1JTGw'
PREFIX_QUERY = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query='

map_type_df = pd.read_csv("../data/google_types.csv", sep=';', )


class GoogleApi:
    def __init__(self, retailer_name, retailer_address):
        self.retailer_name = retailer_name
        self.retailer_address = retailer_address

    def get_place_infos(self):
        query = self.retailer_name + ' ' + self.retailer_address
        return r.get(PREFIX_QUERY + query + '&key=' + KEY_GOOGLE).json()

    def get_place_type_from_google(self, query_result):
        """

        :param query_result: json result from google query
        :return: list of google types
        """
        return query_result['results'][0]['types']

    def convert_googletypes_into_rmwtypes(self, google_list):
        """
        From google types to rmw types
        :param google_list: list of types from google
        :return: list of rmw values
        """
        # list to df
        df_google = pd.DataFrame({'google_names': google_list})
        # merge dfs
        return pd.merge(df_google, map_type_df, left_on='google_names', right_on='google_types', how='left')[
            'rmw_cat'].fillna('').values

    def return_only_one_category(self, list_rmw_cat):
        """
        Choosing among the list the right category.
        In case of equality, alphabetic order is taken
        :param list_rmw_cat: list with various categories
        :return: most occurent value in list, empty are not taken into account
        """
        # Suppress empty items
        list_rmw_cat_not_null = [item for item in list_rmw_cat if item != ""]
        return max(set(list_rmw_cat_not_null), key=list_rmw_cat_not_null.count)
