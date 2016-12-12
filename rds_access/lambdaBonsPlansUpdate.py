from accessRds import AccessRDS
from dynamoDB import AccessDB
from dynamoDBDataPrep import dynamoDBPrep

ards = AccessRDS()
ad = AccessDB()
d = dynamoDBPrep()


def handler(event, context):
    # Get dynamobd data
    input_json = ad.get_item_from_dynamodb()
    print d.from_dynamo_to_mysql(input_json)
    return ards.getBonsPlansInfosRow()
