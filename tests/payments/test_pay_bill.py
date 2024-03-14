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
        'b7de6dbc-df10-4d7b-a2fc-809193ed4c0f',
    ))
    def test_pay_bill(self, bill_id, api_client):
        response = api_client.post(f'/api/v1/bills/{bill_id}/pay/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
