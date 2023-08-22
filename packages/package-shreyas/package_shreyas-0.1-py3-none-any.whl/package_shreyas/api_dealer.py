import pandas as pd
import requests
import json
import hashlib
import datetime

publickey = "31e81875ab9613dcc299cac68e5a7c6a"
privatekey = "bafcb032477dd726c02dd28e792b94390de39f62"
base_url = "http://gateway.marvel.com/v1/public"

ts = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
hash = ts+ privatekey + publickey
md5Hash = hashlib.md5(hash.encode('utf-8')).hexdigest()

params = {
              'ts':ts,
              'apikey':publickey,
              'hash':md5Hash
          }

data_api=[]
offset=0

for i in range(5):

  try:
      response = requests.get(base_url+f"/characters?limit=100&offset={offset}",params=params)
      data_response = response.json()
      data=data_response['data']['results']
      data_api.extend(data)
      offset+=100

  except requests.exceptions.HTTPError as http_err:
      print(f"HTTPError:",{http_err})
  except Exception as err:
      print(f"Error:", {err})

df_marvel_data = pd.json_normalize(data_api)
filter_A = df_marvel_data[df_marvel_data['name'].str.startswith('A')]
print(len(df_marvel_data))
print(len(filter_A))



def marvel_api_call(api_key, hash, base_url, namestartswith=None, length=None):
  data_api=[]
  offset=0
  ts = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
  md5Hash = hash

  params = {
              'ts':ts,
              'apikey':api_key,
              'hash':md5Hash
          }

  if namestartswith:

    params['nameStartsWith']=namestartswith

  for i in range(5):

    try:
        response = requests.get(base_url+f"/characters?limit=100&offset={offset}",params=params)
        response.raise_for_status()
        data_response = response.json()
        data=data_response['data']['results']
        data_api.extend(data)
        offset+=100

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTPError:",{http_err})
    except Exception as err:
        print(f"Error:", {err})

  df_marvel_data = pd.json_normalize(data_api)
  return df_marvel_data


def df_convert(data):

  data_df = pd.json_normalize(data)

  return data_df