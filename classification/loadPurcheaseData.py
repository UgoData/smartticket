# coding: utf-8

# ------ IMPORTS -----
import cPickle as pickle
import json
import re
import warnings

import boto3
import pandas as pd

from tfidf_classification import Classification
from utilNormalizer import Normalizer

print "INTO load purchease"

client = boto3.client('s3', region_name="eu-west-1")
tfidfp = client.get_object(Bucket='smartticket-analytics', Key='dumpTfIdf.pkl')
tf_idf_load_from_pickle = pickle.loads(tfidfp['Body'].read())
rfp = client.get_object(Bucket='smartticket-analytics', Key='dumpRf.pkl')
rf_load_from_pickle = pickle.loads(rfp['Body'].read())
class_client = client.get_object(Bucket='smartticket-analytics', Key='categories.csv')
cat_raw_2 = class_client['Body'].read()


warnings.filterwarnings("ignore")

# input = json.load(open("../data/smart-tickets-payload-example.json", "rb"))
# print input

u = Normalizer()

# Load TF-IDF
# tf_idf_load_from_pickle = pickle.load(open("../models/dumpTfIdf.pkl", "rb"))
# Load Random Forest
# rf_load_from_pickle = pickle.load(open("../models/dumpRf.pkl", "rb"))

BOISSONS_KEYWORDS = ['BOUTEIL', 'PERRIER', 'PELLEGRINO', 'QUEZAC', 'PJ', 'JUS', 'VITTEL', 'BOISS', 'EAU', 'VIN ',
                     'RHUM', 'WHISKY', 'CAFE', 'THE', 'COCA']


class LoadPurchease:
    def __init__(self, input_json):
        self.input_json = input_json

    def extract_description(self, input_json):
        """
        Extraction of the description of the products.
        If ocr processed is not empty then it is a key else we use ocr raw
        :param input: json input from purchease
        :return: dictionary with key equals to production description
        """
        dict_description = {}
        for line in input_json['lines']:
            if line['ocr_processed_description'] != "":
                dict_description[line['ocr_processed_description']] = u.end_to_end_normalize_noaccent(
                    line['category_name'])
            else:
                dict_description[line['ocr_raw_description']] = u.end_to_end_normalize_noaccent(line['category_name'])
        return dict_description

    def classification_homemade(self, input_json):
        """
        Classify the products description into a dictionary.
        The boissons classification is made by hand.
        Not Boissons in learning stage.
        :return: dictionary key: description value : rmw category
        """
        dict_prod = self.extract_description(input_json)

        if len(dict_prod) > 0:
            list_prod = u.from_dict_to_list(dict_prod)
            t = Classification()
            result = t.tfidf_rf_classif_apply(tf_idf_load_from_pickle, rf_load_from_pickle, list_prod)
            list_result = []
            for idx, i in enumerate(result):
                print i
                print list_prod[idx]
                if any(word.lower() in list_prod[idx].lower() for word in BOISSONS_KEYWORDS):
                    list_result.append('boissons')
                else:
                    list_result.append(i)
            return u.from_two_lists_to_dict(list_prod, list_result)
        else:
            return {}

    def fill_input_with_classif(self, input_json):
        """
        Create a json with purchease classification and rmw classification
        :param input_json: json from purchease classification
        :return:
        """
        dict_class = self.classification_homemade(input_json)
        output = {'analytics_result': 'FAILURE', 'smartticket': input_json}
        df_classification = self.get_categories_name_from_csv(cat_raw_2)
        if dict_class != {}:
            for line in input_json['lines']:
                # Creation of a purchease category
                line['category_name_purchease'] = line['category_name']
                # Creation of a rmw category
                if (line['ocr_processed_description'] != ""):
                    print dict_class[line['ocr_processed_description']]
                    line['category_name_rmw'] = self.from_rmwname_to_purcheaseinfos(df_classification, dict_class[
                        line['ocr_processed_description']], 'name_rmw', 'name_purchease')
                else:
                    print dict_class[line['ocr_raw_description']]
                    line['category_name_rmw'] = self.from_rmwname_to_purcheaseinfos(df_classification, dict_class[
                        line['ocr_raw_description']], 'name_rmw', 'name_purchease')
                if (line['category_name'] == 'NON RECONNU') and (line['category_name'] <> line['category_name_rmw']):
                    output['analytics_result'] = 'SUCCESS'
                    line['category_name'] = line['category_name_rmw']
                    line['category_image_url'] = self.from_rmwname_to_purcheaseinfos(df_classification,
                                                                                     line['category_name_rmw'],
                                                                                     'name_purchease', 'img')
                    # TODO : change category_image_url too
        return output

    def good_shape_output_for_post(self, input_json):
        output = input_json.copy()
        for line in output['smartticket']['lines']:
            del line['category_name_purchease']
            del line['category_name_rmw']
        output = u.replace_decimals(output)
        return json.dumps(output)

    def get_categories_name_from_csv(self, cat_raw_2):
        """ return df from a csv located ni s3"""
        line = re.split('\n', cat_raw_2)
        data = []
        for i in line:
            spl = i.split(";")
            data.append([spl[0], spl[1], spl[2]])
        return pd.DataFrame(data, columns=['name_rmw', 'name_purchease', 'img'])

    def from_rmwname_to_purcheaseinfos(self, df, rmw_name, col_to_check, col_to_get):
        print df.loc[df[col_to_check] == rmw_name][col_to_get]
        return df.loc[df[col_to_check] == rmw_name][col_to_get].iloc[0]

        # l = LoadPurchease(input)
        # print l.fill_input_with_classif()
