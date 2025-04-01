import requests
from airtable import Airtable
import os
from os.path import join, dirname
from dotenv import load_dotenv
from tqdm import tqdm

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

base_id = os.environ.get('base_id')
table_name = os.environ.get('table_name')
airtable_token = os.environ.get('airtable_token')
api_key = os.environ.get('api_key')

airtable = Airtable(base_id, table_name, airtable_token)

url = "https://api.clearout.io/v2/email_verify/instant"
headers = {
    'Content-Type': "application/json",
    'Authorization': api_key,
    }

for record in tqdm(airtable.get_all()):
    id = record['id']
    email = record['fields']['Email']
    payload = '{"email": "' + email + '"}'
    response = requests.request("POST", url, data=payload, headers=headers)
    response = response.json()
    if 'data' in response:
        airtable.update(id, {'Status': response['data']['status']})
    else:
        print(response)
        airtable.update(id, {'Status': "error"})
        break