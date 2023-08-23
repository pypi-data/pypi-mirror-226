from IUCN_API.IUCN_API import RedListApiClient

class Groups (RedListApiClient):

    def __init__(self):
        super().__init__()


    """
        View organism comprehensive group
    
    """
    def get_species_group_list(self):
        endpoint = f"{self.base_url}/comp-group/list"
        return self._make_request(endpoint)

    def get_species_by_group_name(self, group_name):
        endpoint = f"{self.base_url}/comp-group/getspecies/{group_name}"
        return self._make_request(endpoint)
    
    