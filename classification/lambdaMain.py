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
    ll = LoadPurchease(event)
    output_full = ll.fill_input_with_classif(event)
    # Save into db
    d.put_item_into_dynamodb(output_full)
    # Clean output for send into post : del purchease_cat and rmw_cat, only stay cat
    return ll.good_shape_output_for_post(output_full)

# print eventHandler(event, 'a')
