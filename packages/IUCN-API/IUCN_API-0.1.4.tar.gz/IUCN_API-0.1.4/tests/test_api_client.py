import pytest
from IUCN_API.modules.Groups import Groups
from IUCN_API.modules.History import History
from IUCN_API.modules.View import View
from IUCN_API.modules.Exceptions.APIKeyException import APIKeyException


@pytest.fixture
def api_client_group():
    return Groups()

@pytest.fixture
def api_client_history():
    return History()

@pytest.fixture
def api_client_view():
    return View()

def test_get_groups(api_client_group):
    data = api_client_group.get_species_group_list()
    assert data


def test_get_view(api_client_view):
    data = api_client_view.get_species_single_by_name("Loxodonta Africana")
    assert data

def test_get_history(api_client_history):
    data = api_client_history.get_species_history_by_name("Loxodonta Africana")
    assert data
