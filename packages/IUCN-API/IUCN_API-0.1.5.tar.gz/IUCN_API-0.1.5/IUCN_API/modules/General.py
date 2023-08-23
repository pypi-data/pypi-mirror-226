from IUCN_API.IUCN_API import RedListApiClient

class General (RedListApiClient):

    def __init__(self):
        super().__init__()


    def get_version (self):
        endpoint = f"{self.base_url}/version"
        return self._make_request(endpoint)

    def get_countries (self):
        endpoint = f"{self.base_url}/country/list"
        return self._make_request(endpoint)
    
    def get_regions (self):
        endpoint = f"{self.base_url}/region/list"
        return self._make_request(endpoint)

    def get_species_by_country(self, country):
        endpoint = f"{self.base_url}/country/getspecies/{country}"
        return self._make_request(endpoint)
    
    def get_species(self, page=1, per_page=10):
        endpoint = f"{self.base_url}/species/page/{page}"
        params = {"page": page, "per_page": per_page}
        return self._make_request(endpoint, params=params)
    
    def get_species_region(self, region_identifier="europe", page=1, per_page=10):
        endpoint = f"{self.base_url}/species/region/{region_identifier}/page/{page}"
        params = {"page": page, "per_page": per_page}
        return self._make_request(endpoint, params=params)
    
    def get_species_count(self):
        endpoint = f"{self.base_url}/speciescount"
        return self._make_request(endpoint)
    
    def get_species_count_by_region(self, region_identifier="europe"):
        endpoint = f"{self.base_url}/speciescount/region/{region_identifier}"
        return self._make_request(endpoint)
    
    def get_species_synonyms_by_name(self, species_name):
        endpoint = f"{self.base_url}/species/synonym/{species_name}"
        return self._make_request(endpoint)
    
    def get_species_common_name_by_name(self, species_name):
        endpoint = f"{self.base_url}/species/common_names/{species_name}"
        return self._make_request(endpoint)

    def get_species_by_category(self, category):
        # check if category exist
        if not category in self.categories:
            return False
        
        endpoint = f"{self.base_url}/species/category/{category}"
        return self._make_request(endpoint)
    
