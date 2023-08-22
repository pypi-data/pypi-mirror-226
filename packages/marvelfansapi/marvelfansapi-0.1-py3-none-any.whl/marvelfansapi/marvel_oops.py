import requests
import pandas as pd

class MarvelAPI:
    def __init__(self, base_url, api_key, hash):
        self.base_url = base_url
        self.api_key = api_key
        self.hash=hash

    def fetch_marvel_characters(self, namestartswith=None,url=None,length=None):
        params={
        "apikey":self.api_key,
        "hash":self.hash,
        "nameStartsWith":namestartswith,
        "length":length
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            characters_data=response.json()["data"]["results"]
            return characters_data
        except: requests.exceptions.HTTPError as http_err:
            raise Exception("HTTP error:" http_err)
        except Exception as err:
            raise Exception("Other error:" err) 

    def create_df(characters_data):
        df = pd.DataFrame(characters_data)
        return df 