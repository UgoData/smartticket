import warnings

from rawTreatment import RawTreatment

warnings.filterwarnings("ignore")

print "INTO LAMBDA ENRICH LOCATION"

# Load python files
r = RawTreatment()


def eventHandler(event, context):
    print "event init :", event
    if event['extraction_type'] == 'RAW':
        return r.create_output(event)
    else:
        return {'smartticket': event, 'analytics_result': 'FAILURE'}


event = {
    'status': 'finished',
    'extraction_type': 'RAW',
    'store_address': {
        'city': None,
        'street_number': None,
        'longitude': None,
        'street': None,
        'latitude': None,
        'zip_code': None
    },
    'uuid': '20161202-1324-5257-72351',
    'light_image_url': 'http://receipts.fidmarques.com/receipts/production/21/2016/12/02/20161202-1324-5257-72351-1/20161202-1324-5257-72351-1_prerotated.jpg',
    'retailer_name': 'Inconnu',
    'lines': [{
        'total_price': None,
        'ocr_processed_description': '01.49.35.88.70',
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }, {
        'total_price': None,
        'ocr_processed_description': 'SAV 01.75.62.26.04',
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }, {
        'total_price': None,
        'ocr_processed_description': "N'SIREN:345197552",
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }, {
        'total_price': None,
        'ocr_processed_description': '**SHEXSHEUS*S***',
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }, {
        'total_price': None,
        'ocr_processed_description': 'Pomses a demaRnder votrne carte de fidelite',
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }, {
        'total_price': None,
        'ocr_processed_description': 'gratuitelll',
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }, {
        'total_price': None,
        'ocr_processed_description': 'Operateur 395 - EREN',
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }, {
        'total_price': None,
        'ocr_processed_description': 'Montant TIC EUR',
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }, {
        'total_price': None,
        'ocr_processed_description': '24646499 LEMON CHAISE PLIANTE 32.99',
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }, {
        'total_price': None,
        'ocr_processed_description': 'Dint part eco-mobilier 0.25 EUR TTC',
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }, {
        'total_price': None,
        'ocr_processed_description': '24646499 LEMON CHAISE PLIANTE 32.99',
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }, {
        'total_price': None,
        'ocr_processed_description': 'Dont PART ECO-Moblier 0.25 EUR TTC',
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }, {
        'total_price': None,
        'ocr_processed_description': 'Total EUR 65.98',
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }, {
        'total_price': None,
        'ocr_processed_description': 'Dont part Eco-mobilier 0.50 EUR TTC',
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }, {
        'total_price': None,
        'ocr_processed_description': 'Tauxs TVA HT TVA TTC',
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }, {
        'total_price': None,
        'ocr_processed_description': '20.00% 54.98 11.00 65.98',
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }, {
        'total_price': None,
        'ocr_processed_description': 'CB Auto 65.98',
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }, {
        'total_price': None,
        'ocr_processed_description': 'Nb Article(s7) : 2',
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }, {
        'total_price': None,
        'ocr_processed_description': "N' de Ticket",
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }, {
        'total_price': None,
        'ocr_processed_description': '0 1216 2470 1132',
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }, {
        'total_price': None,
        'ocr_processed_description': '00012 Poste: 012',
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }, {
        'total_price': None,
        'ocr_processed_description': 'Ecoanse Ou reNDoursement sous 30 jours',
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }, {
        'total_price': None,
        'ocr_processed_description': 'sur Resendedion d 1ice8 de coIsge e',
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }, {
        'total_price': None,
        'ocr_processed_description': "0e : 'emDa.i89e Q o7i9.ne.",
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }, {
        'total_price': None,
        'ocr_processed_description': 'RenDOursement eftecue cdnsle RERe moed',
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }, {
        'total_price': None,
        'ocr_processed_description': 'e re9iemenT.',
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }, {
        'total_price': None,
        'ocr_processed_description': 'LeXCePTIOn POUT IES CheAJES O2I8I MIRImUM',
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }, {
        'total_price': None,
        'ocr_processed_description': '8e 3 9emeIed)',
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }, {
        'total_price': None,
        'ocr_processed_description': 'S>-3-tS t',
        'unit_price': None,
        'ocr_raw_description': None,
        'category_image_url': 'http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png',
        'category_name': 'NON RECONNU',
        'quantity': None
    }
    ],
    'retailer_image_url': 'http://cdn1.skerou.com/images/retailers/inconnu.png',
    'nb_recognized_products': 0,
    'nb_products': 0,
    'date': '02-12-2016 13:24',
    'total': 65.98,
    'user_uuid': 'mtb8@mtb.com'
}

print eventHandler(event, '')
