import requests
import pandas as pd
import datetime
import hashlib

private_key = '7bb43f9cd7777dab93a527edd6ed11feb582bd69'
public_key = 'feb83be881bc549b5354899c7be9a434'

baseURI = "http://gateway.marvel.com/v1/public"
timestamp = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
hash_input = timestamp + private_key + public_key
hashed_string = hashlib.md5(hash_input.encode('utf-8')).hexdigest()
url_params = {
              'ts':timestamp,
              'apikey':public_key,
              'hash':hashed_string
          }

final_list=[]
offset=0

for i in range(5):
  try:
      response = requests.get(baseURI+f"/characters?limit=100&offset={offset}",params=url_params)
      response_data = response.json()
      data=response_data['data']['results']
      final_list.extend(data)
      offset+=100

  except requests.exceptions.HTTPError as http_err:
      print(f"HTTPError:",{http_err})

  except Exception as err:
      print(f"Error:", {err})

marvel_df = pd.json_normalize(final_list)

filtered_char = marvel_df[marvel_df['name'].str.startswith('A')]

len(filtered_char)

from urllib.parse import urlencode

def get_api(baseURI,API_KEY,hash,namestartswith=None,length=None):


  final_list=[]

  offset=0

  params = {

              'ts':timestamp,

              'apikey':API_KEY,

              'hash':hash

          }

  if namestartswith:

    params['nameStartsWith']=namestartswith

  for i in range(5):

    try:

        response = requests.get(baseURI+f"/characters?limit=100&offset={offset}",params=params)
        response.raise_for_status()

        response_data = response.json()

        data=response_data['data']['results']

        final_list.extend(data)

        offset+=100

    except requests.exceptions.HTTPError as http_err:

        print(f"HTTPError:",{http_err})

    except Exception as err:

        print(f"Error:", {err})


def convert_df(data):

  data_df = pd.json_normalize(data)

  return data_df
