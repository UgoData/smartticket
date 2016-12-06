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
        if ('fax' in line_descr) or ('sav' in line_descr):
            return ""
        # Replace letters by nothing
        line_descr = re.sub('\D', '', line_descr)
        # Find number
        m = re.search(
            '\d{2}[-\.\s]??\d{2}[-\.\s]??\d{2}[-\.\s]??\d{2}[-\.\s]??\d{2}|\d{2}?\d{2}?\d{2}?\d{2}?\d{2}|\d{2}[-\ \s]??\d{2}[-\ \s]??\d{2}[-\ \s]??\d{2}[-\ \s]??\d{2}',
            line_descr)
        if m > 0:
            return '.'.join(a + b for a, b in zip(m.group(0)[::2], m.group(0)[1::2]))
        else:
            return ""

    def extract_phone_number_from_lines(self, lines):
        """ Extract phone number from the first line which match """
        for line in lines:
            phone_number = self.extract_phone_number(line['ocr_processed_description'])
            if phone_number != "":
                return phone_number

    def try_google_place(self, list_two_first_lines):
        ## Google place
        g = GoogleApi(list_two_first_lines[0], list_two_first_lines[1])
        result, goog_res_raw = g.google_cat_name_raw()
        if len(result) > 0:
            return result[0], goog_res_raw
        else:
            return '', ''

    def bing_phone_number(self, phone_number):
        keyBing = '4e39f4144f354b388b10566fdb18a882'  # get Bing key from: https://datamarket.azure.com/account/keys
        credentialBing = 'Basic ' + (':%s' % keyBing).encode('base64')[
                                    :-1]  # the "-1" is to remove the trailing "\n" which encode adds
        top = 1

        url = 'https://api.cognitive.microsoft.com/bing/v5.0/search?' + \
              'q=%s&$count=%s&$format=json&$responseFilter=Webpagesfr' % (phone_number, top)
        request = urllib2.Request(url)
        request.add_header('Ocp-Apim-Subscription-Key', keyBing)
        requestOpener = urllib2.build_opener()
        response = requestOpener.open(request)

        results = json.load(response)

        list_results = results['webPages']['value'][:10]
        list_url = []
        for i in list_results:
            list_url.append(i['displayUrl'])
        print list_url
        return list_url

    def extract_request_from_urls(self, list_url):
        res_temp = ' '.join([x
                            .replace('/', ' ')
                            .replace('.', ' ')
                            .replace('_', ' ')
                            .replace('-', ' ')
                            .replace('?', ' ')
                            .replace('=', ' ') for x in list_url])
        stop_words = ['http:', 'https:', 'www', 'fr', 'com', 'html', 'annuaire', 'france', 'pagesjaunes']
        text = ' '.join([word.lower() for word in res_temp.split() if word not in stop_words])
        # print text
        dict_res = Counter(text.split(' '))
        sorted_x = sorted(dict_res.items(), key=operator.itemgetter(1), reverse=True)[:4]
        print sorted_x
        final_res = ' '.join([k for (k, v) in sorted_x])
        print final_res
        return final_res

    def split_adress(self, formatted_address):
        num_street = formatted_address.split(',')[0]
        zip_city = formatted_address.split(',')[1]
        street = re.sub('[\d ]', '', num_street)
        num = re.sub('\D', '', num_street)
        city = re.sub('[\d ]', '', zip_city)
        zipcode = re.sub('\D', '', zip_city)
        return num, street, zipcode, city

    def extract_adress_from_google_raw(self, google_raw):
        result_adress = {}
        if 'formatted_address' in google_raw:
            format_address = google_raw['formatted_address']
        if ('geometry' in google_raw) and ('location' in google_raw['geometry']):
            lat = google_raw['geometry']['location']['lat']
            long = google_raw['geometry']['location']['long']

    def create_output(self, event):
        output = {'analytics_result': 'FAILURE'}
        result_event = event
        # Empty line
        lines = []
        # Empty retailer_name
        retailer_name = ''
        # First try google
        list_two_first_lines = self.extract_first_lines(event)
        res_google_1, google_raw_1 = self.try_google_place(list_two_first_lines)
        line = {}
        if res_google_1 != '':
            line['ocr_processed_description'] = res_google_1
            line['unit_price'] = event['total']
            line['total_price'] = event['total']
            line['quantity'] = 1
            line['category_name'] = res_google_1
            line['ocr_raw_description'] = ''
            line['category_image_url'] = google_raw_1['icon']
            lines.append(line)
            retailer_name = google_raw_1['name']
        else:
            phone_number = self.extract_phone_number_from_lines(event['lines'])
            list_url = self.bing_phone_number(phone_number)
            request_google = self.extract_request_from_urls(list_url)
            res_google_2, google_raw_2 = self.try_google_place([request_google, ''])
            if res_google_2 != '':
                line['ocr_processed_description'] = res_google_2
                line['unit_price'] = event['total']
                line['total_price'] = event['total']
                line['quantity'] = 1
                line['category_name'] = res_google_2
                line['ocr_raw_description'] = ''
                line['category_image_url'] = google_raw_2['icon']
                lines.append(line)
                retailer_name = google_raw_2['name']
            else:
                lines = event['lines']

        # Fill output
        if len(lines) == 1:
            output['analytics_result'] = 'SUCCESS'
            result_event['lines'] = lines
            result_event['retailer_name'] = retailer_name

        output['smartticket'] = result_event
        return output
