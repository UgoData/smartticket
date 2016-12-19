import json
import operator
import re
import urllib2
from collections import Counter

from googlePlaces import GoogleApi


class RawTreatment:
    def __init__(self):
        self

    def extract_first_lines(self, event):
        return [line['ocr_processed_description'] for line in event['lines'][:2]]

    def extract_phone_number(self, line_descr):
        # Pre process : identify number
        line_descr = line_descr.lower()
        # print line_descr
        if ('fax' in line_descr) or ('sav' in line_descr):
            return ""
        # Replace letter o by zero
        line_descr = re.sub('o', '0', line_descr)
        # Replace letters by nothing
        line_descr = re.sub('\D', '', line_descr)
        # print line_descr
        # Find number
        m = re.search(
            '^\d{2}?\d{2}?\d{2}?\d{2}?\d{2}$|^\d{2}[.]?\d{2}[.]?\d{2}[.]?\d{2}[.]?\d{2}$',
            line_descr)
        if m > 0:
            tel = '.'.join(a + b for a, b in zip(m.group(0)[::2], m.group(0)[1::2]))
            if tel[0] == '0':
                print 'Telephone number :', tel
                return tel
            else:
                return ""
        else:
            return ""

    def extract_phone_number_from_lines(self, lines):
        """ Extract phone number from the first line which match """
        for line in lines:
            phone_number = self.extract_phone_number(line['ocr_processed_description'])
            if phone_number != "":
                return phone_number

    def extract_total(self, total_field, lines):
        if (total_field is None) or (total_field == 0.0):
            for l in lines:
                ll = l['ocr_processed_description'].lower()
                extract_total = re.search('(\d+[.]\d+)', ll)
                if ('tot' in ll or 'ttc' in ll) and ('ht' not in ll) and ('h.t' not in ll) and ('sous' not in ll) and (
                    'ss' not in ll) and (extract_total > 0):
                    return float(extract_total.group(0))
        return total_field


    def try_google_place(self, list_two_first_lines):
        ## Google place
        g = GoogleApi(list_two_first_lines[0], list_two_first_lines[1])
        result, goog_res_raw = g.google_cat_name_raw()
        if len(result) > 0:
            return result[0], goog_res_raw
        else:
            return '', ''

    def bing_phone_number(self, phone_number):
        print 'PHONE NUMBER :', phone_number
        keyBing = '5c8a174f359044099bf1e93dc93b703b'  # get Bing key from: https://datamarket.azure.com/account/keys
        credentialBing = 'Basic ' + (':%s' % keyBing).encode('base64')[
                                    :-1]  # the "-1" is to remove the trailing "\n" which encode adds
        top = 1

        url = 'https://api.cognitive.microsoft.com/bing/v5.0/search?' + \
              'q=%s&$count=%s&$format=json&$responseFilter=Webpages&mkt=fr-FR' % (phone_number, top)
        request = urllib2.Request(url)
        request.add_header('Ocp-Apim-Subscription-Key', keyBing)
        requestOpener = urllib2.build_opener()
        response = requestOpener.open(request)

        results = json.load(response)
        # print results
        list_url = []
        if 'webPages' in results:
            list_results = results['webPages']['value'][:10]
            for i in list_results:
                list_url.append(i['name'])
        # print list_url
        return list_url

    def extract_request_from_urls(self, list_url):
        res_temp = ' '.join([x
                            .replace('/', ' ')
                            .replace('.', ' ')
                            .replace('_', ' ')
                            .replace('-', ' ')
                            .replace('?', ' ')
                            .replace('=', ' ') for x in list_url])
        stop_words = ['http:', 'https:', 'www', 'fr', 'com', 'html', 'annuaire', 'france', 'pagesjaunes', 'le', 'la',
                      'de', 'du', 'des']
        text = ' '.join([word.lower() for word in res_temp.split() if word not in stop_words])
        # print text
        dict_res = Counter(text.split(' '))
        sorted_x = sorted(dict_res.items(), key=operator.itemgetter(1), reverse=True)[:10]
        print sorted_x
        final_res = ' '.join([k for (k, v) in sorted_x if v > 2])
        print final_res
        return final_res

    def split_adress(self, formatted_address):
        num_street = formatted_address.split(',')[0]
        zip_city = formatted_address.split(',')[1]
        street = re.sub('^(\s+)', '', re.sub('[\d]', '', num_street))
        num = re.sub('\D', '', num_street)
        city = re.sub('[\d ]', '', zip_city)
        zipcode = re.sub('\D', '', zip_city)
        return num, street, zipcode, city

    def extract_address_from_google_raw(self, google_raw, result_address):
        if ('formatted_address' in google_raw) and (result_address['city'] is None or result_address['city'] == ''):
            format_address = google_raw['formatted_address']
            result_address['street_number'], result_address['street'], result_address['zip_code'], result_address[
                'city'] = self.split_adress(format_address)
        return result_address

    def extract_latlong_from_google_raw(self, google_raw, result_address):
        if ('geometry' in google_raw) and ('location' in google_raw['geometry']) and (
                result_address['latitude'] is None or result_address['latitude'] == ''):
            result_address['latitude'] = google_raw['geometry']['location']['lat']
            result_address['longitude'] = google_raw['geometry']['location']['lng']
        return result_address

    def create_output(self, event):
        output = {'analytics_result': 'FAILURE'}
        result_event = event
        # Empty line
        lines = []
        # Empty retailer_name
        retailer_name = ''
        # Empty address
        address = {}
        # Empty total
        total = event['total']
        # First try google
        list_two_first_lines = self.extract_first_lines(event)
        res_google_1, google_raw_1 = self.try_google_place(list_two_first_lines)
        line = {}
        if res_google_1 != '':
            print 'Process : GOOGLE PLACES'
            total = self.extract_total(event['total'], event['lines'])
            line['ocr_processed_description'] = res_google_1
            line['unit_price'] = total
            line['total_price'] = total
            line['quantity'] = 1
            line['category_name'] = res_google_1
            line['ocr_raw_description'] = ''
            line['category_image_url'] = google_raw_1['icon']
            lines.append(line)
            retailer_name = google_raw_1['name']
            address = self.extract_address_from_google_raw(google_raw_1, event['store_address'])
            address = self.extract_latlong_from_google_raw(google_raw_1, address)

        else:
            'Process PHONE NUMBER'
            phone_number = self.extract_phone_number_from_lines(event['lines'])
            list_url = self.bing_phone_number(phone_number)
            request_google = self.extract_request_from_urls(list_url)
            res_google_2, google_raw_2 = self.try_google_place([request_google, ''])
            if res_google_2 != '':
                'Process GOOGLE PLACE via PHONE NUMBER'
                total = self.extract_total(event['total'], event['lines'])
                line['ocr_processed_description'] = res_google_2
                line['unit_price'] = total
                line['total_price'] = total
                line['quantity'] = 1
                line['category_name'] = res_google_2
                line['ocr_raw_description'] = ''
                line['category_image_url'] = google_raw_2['icon']
                lines.append(line)
                retailer_name = google_raw_2['name']
                address = self.extract_address_from_google_raw(google_raw_2, event['store_address'])
                address = self.extract_latlong_from_google_raw(google_raw_2, address)
            else:
                lines = event['lines']

        # Fill output
        result_event['total'] = total
        if len(lines) == 1:
            output['analytics_result'] = 'SUCCESS'
            result_event['lines'] = lines
            result_event['retailer_name'] = retailer_name
            result_event['store_address'] = address


        output['smartticket'] = result_event
        return output




r = RawTreatment()
print r.extract_phone_number('TEL:O1 45 26 62 46')
# result_bing = r.extract_request_from_urls(r.bing_phone_number('01.40.06.08.80'))
# print result_bing
# print r.try_google_place([result_bing, ''])
#
# event = {
# "status": "finished",
# "extraction_type": "RAW",
# "total": 2.1,
# "uuid": "20161209-1558-2474-62401",
# "retailer_name": "Inconnu",
# "lines": [{
#         "total_price": None,
#         "ocr_processed_description": "Date: 20/07/2016 18:32 Nb Article: 1",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "Caisse: 367 Ticket: 6202208",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "94459",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "Vendeur : 94459",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "ZONE 152",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "2069891938579 2213 PIERRE HERME 5 5 %",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "Article PRouge",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "= 2.10 \\u20ac",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "Total 2.10 \\u20ac",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "Especes : 2.10 \\u20ac",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "Taux TVA Montant H T T.V.A.",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "5.50 % 1.99 \\u20ac 0.11 \\u20ac",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "M E R C T",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "A bientot en magasin et",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "sur galerieslafayette.com",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "\\ Veuillez faire la detaxe ",
#         " unit_price ": None,
#         " ocr_raw_description ": None,
#         " category_image_url ": " http: //cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "1e Jour de voire achat",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "\\ Please do your Tax Refund",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "on the day of your purchase.\\",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "Echanse oUu remboursement jsous 30 jours",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "sur presentation du ticket de coisse.",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "*5saut eXCePtion 5i9naoiees en ha983slrn",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "Exchange or refund within 30 days*",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "days With a valid receipi",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "*ReXCePtion 5tore",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "GL HAUSSMANN",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "40 bId Haussnenn",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "75446 PARIS CEDEX 09",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "Tel 01.42.82.34.56",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "Du lundi au samedi 9h30-20h",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "et le jeudi 9h30-20hM30.",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "367620220812",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "RCS Paris: 572 062 594 Cap: 217 404 572\\u20ac",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "TVA Intracom FR65 572 062 594",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }, {
#         "total_price": None,
#         "ocr_processed_description": "Mhe9asin GL HAUSSMANN",
#         "unit_price": None,
#         "ocr_raw_description": None,
#         "category_image_url": "http://cdn1.skerou.com/images/products/skerou_created/unknown_product.png",
#         "quantity": None,
#         "category_name": "NON RECONNU"
#     }
# ],
# "retailer_image_url": "http://cdn1.skerou.com/images/retailers/inconnu.png",
# "date": "20-07-2016 18:32",
# "nb_products": 0,
# "nb_recognized_products": 0,
# "store_address": {
#     "latitude": None,
#     "city": None,
#     "street": None,
#     "longitude": None,
#     "zip_code": None
# },
# "light_image_url": "http://receipts.fidmarques.com/receipts/production/21/2016/12/09/20161209-1558-2474-62401-1/20161209-1558-2474-62401-1_prerotated.jpg",
# "user_uuid": "marine.lebez@gmail.com"
# }
#
#
#
# r.create_output( event)
