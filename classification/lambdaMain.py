import json
import warnings

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
event = json.load(open("../data/smart-tickets-payload-example.json", "rb"))


# print input

def eventHandler(event, context):
    print "event init :", event
    ll = LoadPurchease(event)
    return ll.fill_input_with_classif(event)


print eventHandler(event, 'a')
