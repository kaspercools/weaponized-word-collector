import json 
import requests
import os

base_path = 'https://api.weaponizedword.org/lexicons/1-0/'
api_key = os.getenv('WW_API_KEY')
base_data_dir = 'lexicons'

authentication_payload= { 'api_key':api_key }
auth_response = requests.post(base_path+'authenticate', data = authentication_payload)
auth_response = auth_response.json()

request_token = auth_response['result']['token']

# we have the request token -> now let's gather the data
terms = ['watchwords']

# categories to be queried
retainable_levels_of_offensiveness = ['Mildly offensive or inoffensive','Extremely offensive', 'Very offensive', 'Significantly offensive', 'Moderately offensive', 'Midly offensive']

def process_batch(term, result):
    data_dir = base_data_dir +'/'+ term+'/'

    for word in result:
        if(word['offensiveness'] in retainable_levels_of_offensiveness):
            print(word['term_id'])
            with open(data_dir+word['term_id']+'.json', 'w') as outfile:
                outfile.write(json.dumps(word))

def retrieveLexicon(term):
    number_of_pages  = 1
    current_page = 1
    while(current_page <= number_of_pages):
        query_payload = { 'token':request_token, 'page':current_page, 'language_id':'eng' }
        query_request = requests.post(base_path + 'get_discriminatory', data =query_payload)
        query_result = query_request.json()
        number_of_pages = query_result['number_of_pages']
        current_page += 1
        process_batch(term, query_result['result'])

for term in terms:
    retrieveLexicon(term)
