# coding: utf-8

# ------ IMPORTS -----
import cPickle as pickle
import warnings

import boto3

from tfidf_classification import Classification
from utilNormalizer import Normalizer

print "INTO load purchease"

client = boto3.client('s3', region_name="eu-west-1")
tfidfp = client.get_object(Bucket='smartticket-analytics', Key='dumpTfIdf.pkl')
tf_idf_load_from_pickle = pickle.loads(tfidfp['Body'].read())
rfp = client.get_object(Bucket='smartticket-analytics', Key='dumpRf.pkl')
rf_load_from_pickle = pickle.loads(rfp['Body'].read())


warnings.filterwarnings("ignore")

# input = json.load(open("../data/smart-tickets-payload-example.json", "rb"))
# print input

u = Normalizer()

# Load TF-IDF
# tf_idf_load_from_pickle = pickle.load(open("../models/dumpTfIdf.pkl", "rb"))
# Load Random Forest
# rf_load_from_pickle = pickle.load(open("../models/dumpRf.pkl", "rb"))


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
                dict_description[line['ocr_processed_description']] = line['category_name']
            else:
                dict_description[line['ocr_raw_description']] = line['category_name']
        return dict_description

    def classification_homemade(self, input_json):
        """
        Classify the products description into a dictionary
        :return: dictionary key: description value : rmw category
        """
        dict_prod = self.extract_description(input_json)
        list_prod = u.from_dict_to_list(dict_prod)
        t = Classification()
        result = t.tfidf_rf_classif_apply(tf_idf_load_from_pickle, rf_load_from_pickle, list_prod)
        return u.from_two_lists_to_dict(list_prod, result)

    def fill_input_with_classif(self, input_json):
        """
        Create a json with purchease classification and rmw classification
        :param input_json: json from purchease classification
        :return:
        """
        dict_class = self.classification_homemade(input_json)
        output = {'analytics_result': 'FAILURE', 'smartticket': input_json}
        for line in input_json['lines']:
            # Creation of a purchease category
            line['category_name_purchease'] = line['category_name']
            # Creation of a rmw category
            if (line['ocr_processed_description'] != ""):
                line['category_name_rmw'] = dict_class[line['ocr_processed_description']].upper()
            else:
                line['category_name_rmw'] = dict_class[line['ocr_raw_description']].upper()
            if (line['category_name'] == 'NON RECONNU') and (line['category_name'] <> line['category_name_rmw']):
                    output['analytics_result'] = 'SUCCESS'
                    line['category_name'] = line['category_name_rmw']
                    # TODO : change category_image_url too
        return output

    def good_shape_output_for_post(self, input_json):
        output = input_json.copy()
        for line in input_json['lines']:
            del line['category_name_purchease']
            del line['category_name_rmw']
        return

        # l = LoadPurchease(input)
        # print l.fill_input_with_classif()
