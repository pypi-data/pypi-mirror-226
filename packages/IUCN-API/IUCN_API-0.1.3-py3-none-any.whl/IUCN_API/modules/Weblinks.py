from IUCN_API.IUCN_API import RedListApiClient

class Weblinks (RedListApiClient):

    def __init__(self):
        super().__init__()
    
    """
        Weblink for Red list 
    
    """
    def get_red_list_website_link_name(self, species_name:str=""):
        endpoint = f"{self.base_url}/weblink/{species_name}"
        return self._make_request(endpoint)

    def get_red_list_website_redirect_name(self, species_name:str=""):
        endpoint = f"{self.base_url}/website/{species_name}"
        return self._make_request(endpoint)
    
    def get_red_list_website_link_id(self, taxon_id:int=""):
        endpoint = f"{self.base_url}/taxonredirect/{taxon_id}"
        return self._make_request(endpoint)

    def get_red_list_website_redirect_id(self, taxon_id:int="", region_identifier:str=""):
        endpoint = f"{self.base_url}/taxonredirect/{taxon_id}/{region_identifier}"
        return self._make_request(endpoint)