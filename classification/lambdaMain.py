import json
import warnings

import boto3

from dynamoDB import AccessDB
from loadAndCleanData import LoadCleanData
from loadPurcheaseData import LoadPurchease
from processTextData import ProcessText
from utilNormalizer import Normalizer

warnings.filterwarnings("ignore")

print "INTO LAMBDA"

# Load python files
p = ProcessText()
l = LoadCleanData()
u = Normalizer()


# Load data for test
# event = json.load(open("../data/smart-tickets-payload-example.json", "rb"))


# print input

lambda_client = boto3.client('lambda', region_name="eu-west-1")

def eventHandler(event, context):
    print "event init :", event
    d = AccessDB(event['stageVariables'])

    event_bytes = json.dumps(event['body'])
    function_name = event['stageVariables']['stage'] + '-' + "smartticket-location"
    invoke_response = lambda_client.invoke(FunctionName=function_name,
                                           InvocationType='RequestResponse',
                                           Payload=event_bytes)
    new_event = invoke_response['Payload'].read()
    print "New event : ", new_event
    new_event_smartt = json.loads(new_event)['smartticket']
    new_event_smartt = replace_empty_string(new_event_smartt)

    if new_event_smartt['extraction_type'] == 'STRUCTURED':
        ll = LoadPurchease(new_event_smartt)
        output_full = ll.fill_input_with_classif(new_event_smartt)
        # Save into db
        d.put_item_into_dynamodb(output_full)
        # Clean output for send into post : del purchease_cat and rmw_cat, only stay cat
        return respond('', ll.good_shape_output_for_post(output_full))
    else:
        return respond('', new_event)


def respond(err, res=None):
    return {
        'statusCode': '404' if err else '200',
        'body': json.dumps(err) if err else res,
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def replace_empty_string(obj):
    if isinstance(obj, list):
        for i in xrange(len(obj)):
            obj[i] = replace_empty_string(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in obj.iterkeys():
            obj[k] = replace_empty_string(obj[k])
        return obj
    elif isinstance(obj, (str, unicode)):
        print(obj)
        if not obj:
            return None
        else:
            return obj
    else:
        return obj

        # event = {
        # 	'status': 'finished',
        # 	'extraction_type': 'STRUCTURED',
        # 	'total': 36.14,
        # 	'uuid': '20161109-0959-9752-402881196-1',
        # 	'retailer_name': 'Carrefour',
        # 	'lines': [{
        # 			'total_price': 7.1,
        # 			'ocr_processed_description': 'CHAUSSON FRUIT',
        # 			'unit_price': 3.05,
        # 			'ocr_raw_description': 'CHAOSSON FROIT',
        # 			'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        # 			'quantity': 2,
        # 			'category_name': 'NON RECONNU'
        # 		}, {
        # 			'total_price': 1.59,
        # 			'ocr_processed_description': 'BOUTEILLE 33CL',
        # 			'unit_price': 1.59,
        # 			'ocr_raw_description': 'BOUTEILLE 33CL',
        # 			'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        # 			'quantity': 1,
        # 			'category_name': 'NON RECONNU'
        # 		}
        # 	],
        # 	'retailer_image_url': 'http://cdn1.skerou.com/images/retailers/carrefour.png',
        # 	'date': '09-11-2016 09:59',
        # 	'nb_products': 7,
        # 	'nb_recognized_products': 0,
        # 	'store_address': {
        # 		'city': 'Paris',
        # 		'street_number': '150',
        # 		'longitude': '3.234567890987654',
        # 		'street': 'rue du Faubourg Poissonniere',
        # 		'latitude': '2.2345678909876543',
        # 		'zip_code': '75010'
        # 	},
        # 	'light_image_url': 'http://receipts.fidmarques.com/receipts/production/21/2016/11/09/20161109-0959-9752-402881196-1/20161109-0959-9752-402881196-1_prerotated.jpg',
        # 	'user_uuid': '123456789'
        # }
        #
        #
        # print eventHandler(event, '')
