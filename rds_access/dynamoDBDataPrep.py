import re

import boto3
import pandas as pd

client = boto3.client('s3', region_name="eu-west-1")
class_client = client.get_object(Bucket='smartticket-analytics', Key='correspondance_bonsplans.csv')
cat_raw = class_client['Body'].read()


class dynamoDBPrep:
    def __init__(self):
        self

    def from_dynamo_to_mysql(self, input_json):
        # Convert json to df
        list_data = []
        for ticket in input_json:
            store_name = ticket['retailer_name']
            for line in ticket['lines']:
                cat = line['category_name_purchease']
                prod_descr = line['ocr_processed_description']
                list_data.append([cat, prod_descr, store_name])
        df = pd.DataFrame(list_data, columns=['category', 'product_descr', 'store'])
        print df.head()
        return df

    def get_bonsplans_nomencl(self, cat_raw):
        """ return df from a csv located ni s3"""
        line = re.split('\n', cat_raw)
        data = []
        for i in line:
            spl = i.split(";")
            data.append([spl[0], spl[1]])
        return pd.DataFrame(data, columns=['cat_name', 'bonsplans_id'])

    def get_bonsplans_nomencl(self, cat_raw):
        """ return df from a csv located ni s3"""
        line = re.split('\n', cat_raw)
        data = []
        for i in line:
            spl = i.split(";")
            data.append([spl[0], spl[1]])
        return pd.DataFrame(data, columns=['cat_name', 'bonsplans_id'])



        # dynamoDBPrep().from_dynamo_to_mysql(AccessDB().get_item_from_dynamodb())
