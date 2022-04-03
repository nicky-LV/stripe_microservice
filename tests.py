import json
from fastapi.testclient import TestClient
from .main import app
from .schemas import StripeProduct


client = TestClient(app)


def test_create_checkout_session():
    pass


def test_create_product():
    # No ID specified, Stripe will provide a random ID for this test product.
    test_product = StripeProduct(name="test_product", description="test_product", shippable=True,
                                 url="https://test_url.com")

    response = client.get("/create-product", data=json.dumps(test_product.dict()))

    assert response.status_code == 201
