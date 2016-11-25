import decimal

import boto3

client = boto3.client('dynamodb')
table = boto3.resource('dynamodb').Table('analytics-smartticket')


class AccessDB:
    def __init__(self, json_input):
        self.json_input = json_input

    def replace_floats(self, obj):
        if isinstance(obj, list):
            for i in xrange(len(obj)):
                obj[i] = self.replace_floats(obj[i])
            return obj
        elif isinstance(obj, dict):
            for k in obj.iterkeys():
                obj[k] = self.replace_floats(obj[k])
            return obj
        elif isinstance(obj, float):
            if obj % 1 == 0:
                return int(obj)
            else:
                return decimal.Decimal(str(obj))
        else:
            return obj

    def replace_decimals(self, obj):
        if isinstance(obj, list):
            for i in xrange(len(obj)):
                obj[i] = self.replace_decimals(obj[i])
            return obj
        elif isinstance(obj, dict):
            for k in obj.iterkeys():
                obj[k] = self.replace_decimals(obj[k])
            return obj
        elif isinstance(obj, decimal.Decimal):
            if obj % 1 == 0:
                return int(obj)
            else:
                return float(obj)
        else:
            return obj

    def put_item_into_dynamodb(self, json_input):
        table.put_item(Item=self.replace_floats(json_input))
        return "Item {} saved into db", json_input['uuid']

    def get_item_from_dynamodb(self):
        smartticket = table.get_item(Key=uuid)
        if 'Item' in smartticket:
            return self.replace_decimals(smartticket['Item'])
        else:
            return None
