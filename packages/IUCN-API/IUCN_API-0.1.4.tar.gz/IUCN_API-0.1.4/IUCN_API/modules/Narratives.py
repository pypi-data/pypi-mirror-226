from IUCN_API.IUCN_API import RedListApiClient

class Narratives (RedListApiClient):

    def __init__(self):
        super().__init__()

    """
        View organism narrative information using name, id and region identifier
    
    """


    def get_species_narrative_by_name(self, species_name):
        endpoint = f"{self.base_url}/species/narrative/{species_name}"
        return self._make_request(endpoint)
    
    def get_species_narrative_by_name_by_region(self, species_name, region_identifier="europe"):
        endpoint = f"{self.base_url}/species/narrative/{species_name}/region/{region_identifier}"
        return self._make_request(endpoint)
    

    def get_species_narrative_by_id(self, species_id):
        endpoint = f"{self.base_url}/species/narrative/id/{species_id}"
        return self._make_request(endpoint)
    
    def get_species_narrative_by_id_by_region(self, species_id, region_identifier="europe"):
        endpoint = f"{self.base_url}/species/narrative/id/{species_id}/region/{region_identifier}"
        return self._make_request(endpoint)
