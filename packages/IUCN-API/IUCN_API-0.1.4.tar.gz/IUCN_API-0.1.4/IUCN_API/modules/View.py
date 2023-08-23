from IUCN_API.IUCN_API import RedListApiClient

class View (RedListApiClient):

    def __init__(self):
        super().__init__()

    """
        View organism  using name, id and region identifier
    
    """


    def get_species_single_by_name(self, species_name):
        endpoint = f"{self.base_url}/species/{species_name}"
        return self._make_request(endpoint)
    
    def get_species_single_by_name_by_region(self, species_name, region_identifier="europe"):
        endpoint = f"{self.base_url}/species/{species_name}/region/{region_identifier}"
        return self._make_request(endpoint)
    
    def get_species_single_by_id(self, species_id):
        endpoint = f"{self.base_url}/species/{species_id}"
        return self._make_request(endpoint)
    
    def get_species_single_by_id_by_region(self, species_id, region_identifier="europe"):
        endpoint = f"{self.base_url}/species/{species_id}/region/{region_identifier}"
        return self._make_request(endpoint)
    