import warnings

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
d = AccessDB()

# Load data for test
# event = json.load(open("../data/smart-tickets-payload-example.json", "rb"))


# print input

def eventHandler(event, context):
    print "event init :", event
    if event['extraction_type'] == 'STRUCTURED':
        ll = LoadPurchease(event)
        output_full = ll.fill_input_with_classif(event)
        # Save into db
        d.put_item_into_dynamodb(output_full)
        # Clean output for send into post : del purchease_cat and rmw_cat, only stay cat
        return ll.good_shape_output_for_post(output_full)
    else:
        return {'smartticket': event, 'analytics_result': 'FAILURE'}

# print eventHandler({
#   "status": "finished",
#   "uuid": "20161109-0959-9752-402881196-1",
#   "retailer_name": "Carrefour",
#   "retailer_image_url": "http://cdn1.skerou.com/images/retailers/carrefour.png",
#   "light_image_url": "http://receipts.fidmarques.com/receipts/production/21/2016/11/09/20161109-0959-9752-402881196-1/20161109-0959-9752-402881196-1_prerotated.jpg",
#   "extraction_type": "STRUCTURED",
#   "nb_products": 7,
#   "nb_recognized_products": 0,
#   "total": 36.14,
#   "date": "09-11-2016 09:59",
#   "user_uuid": "123456789",
#   "store_address": {
#     "street_number": "150",
#     "street": "rue du Faubourg Poissonniere",
#     "city": "Paris",
#     "zip_code": "75010",
#     "latitude": "2.2345678909876543",
#     "longitude": "3.234567890987654"
#   },
#   "lines": [
#     {
#       "ocr_raw_description": "CHAOSSON FROIT",
#       "ocr_processed_description": "CHAUSSON FRUIT",
#       "quantity": 2,
#       "unit_price": 3.05,
#       "total_price": 7.1,
#       "category_name": "NON RECONNU",
#       "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png"
#     },
#     {
#       "ocr_raw_description": "BOUTEILLE 33CL",
#       "ocr_processed_description": "BOUTEILLE 33CL",
#       "quantity": 1,
#       "unit_price": 1.59,
#       "total_price": 1.59,
#       "category_name": "NON RECONNU",
#       "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png"
#     }
#   ]
# }, 'a')
