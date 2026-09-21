import pytest
from playwright.sync_api import expect

from clients.snagly_api import SnaglyApi


@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.case_id("SNAG-TC-030")
def test_public_plans_endpoint_is_available(api_client):
    response = SnaglyApi(api_client).get_public_plans()
    expect(response).to_be_ok()
    assert "data" in response.json()
