
import requests
import pandas as pd
import datetime
import hashlib

class API:
  def fetch_data(self,api_key, hash, namestartswith=None, URI=None, length=None):

    private_key = 'a16c97622089e1bdffec4d72216cbeed53ad7fb4'
    public_key = '4b21b06c3f23788e0698a62cf3d42d1c'
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
    return final_list


  def convert_to_dataframe(self, data):
    data_df = pd.json_normalize(data)
    data_df.replace('null',None,inplace=True)
    return data_df

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