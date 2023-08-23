import os
import requests
from dotenv import load_dotenv
from IUCN_API.Exceptions.APIKeyException import APIKeyException


# Load variables from .env into environment
load_dotenv()

class RedListApiClient:
    def __init__(self):
        # Read environment variable
        api_key = os.getenv("API_KEY")
        if (not api_key or api_key == ""):
            raise APIKeyException("API |Key has not been set. Add API_KEY = '' in your .env file")
        
        self.base_url = "https://apiv3.iucnredlist.org/api/v3"
        self.api_key = api_key
        self.categories = {
            "DD": "DD", "LC": "LC", "NT": "NT", 
            "VU": "VU", "EN": "EN", "CR": "CR", 
            "EW": "EW", "EX": "EX", "LRlc": "LR/lc", 
            "LRnt": "LR/nt", "LRcd": "LR/cd"
        }

    def _make_request(self, endpoint, params=None):
        params = params or {}
        params["token"] = self.api_key
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    
    

    

    
    

    

    

    
    


    

    
    
    
