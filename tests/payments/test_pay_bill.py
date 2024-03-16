import pytest
from rest_framework import status


@pytest.mark.django_db
class BillViewTest:

    @pytest.fixture(autouse=True)
    def loaddata(self, load_fixtures):
        load_fixtures(
            'users.json', 'products.json', 'seller_products.json', 'orders.json', 'bills.json'
        )

    @pytest.mark.parametrize('bill_id', (
        'cfd4b92c-3299-402b-b69d-5a2460a1783d',
    ))
    def test_pay_bill(self, bill_id, api_client):
        response = api_client.post(f'/api/v1/bills/{bill_id}/pay/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
