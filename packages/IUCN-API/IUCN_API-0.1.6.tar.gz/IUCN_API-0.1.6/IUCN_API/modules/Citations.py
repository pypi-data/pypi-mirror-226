from IUCN_API.IUCN_API import RedListApiClient

class Citations (RedListApiClient):

    def __init__(self):
        super().__init__()

    """
        View organism citations using name, id and region identifier
    
    """

    def get_species_citation_by_name(self, species_name="loxodonta africana"):
        endpoint = f"{self.base_url}/species/citation/{species_name}"
        return self._make_request(endpoint)
    
    def get_species_citation_region_by_name(self, region_identifier="europe", species_name="loxodonta africana"):
        endpoint = f"{self.base_url}/species/citation/{species_name}/region/{region_identifier}"
        return self._make_request(endpoint)
    
    def get_species_citation_by_id(self, species_id="299929"):
        endpoint = f"{self.base_url}/species/citation/{species_id}"
        return self._make_request(endpoint)
    
    def get_species_citation_region_by_id(self, region_identifier="europe", species_id="9929292"):
        endpoint = f"{self.base_url}/species/citation/{species_id}/region/{region_identifier}"
        return self._make_request(endpoint)
    