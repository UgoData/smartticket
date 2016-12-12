import json
import warnings

from rawTreatment import RawTreatment

warnings.filterwarnings("ignore")

print "INTO LAMBDA ENRICH LOCATION PLACE"

# Load python files
r = RawTreatment()


def eventHandler(event, context):
    print "event init :", event
    print type(event)
    event = json.loads(event)

    if event['extraction_type'] == 'RAW':
        result = r.create_output(event)
        print result
        return result
    else:
        return {'smartticket': event, 'analytics_result': 'FAILURE'}


