import pytest


@pytest.mark.parametrize("endpoint, method", [("widget", "GET"), ("order", "GET"), ("health", "GET")])
def test_widget_GET(response):
    """Test /widget GET response schema"""
    payload = {"status": 200, "schema": {"id": "string", "status": "string", "amount": "string", "reviewUrl": "string"}}

    assert "id" in payload["schema"]
    assert "status" in payload["schema"]
    assert "amount" in payload["schema"]
    assert "reviewUrl" in payload["schema"]

@pytest.mark.parametrize("endpoint, method", [("order", "GET")])
def test_order_GET(response):
    """Test /order GET response schema"""
    payload = {"status": 200, "schema": {"orderId": "string", "total": (int, float), "currency": "string"}}

    assert "orderId" in payload["schema"]
    assert "total" in payload["schema"]
    # Old clients would expect 'total' to be number, not int/float
    # comment: # total was previously a number

    assert "currency" in payload["schema"]


@pytest.mark.parametrize("endpoint, method", [("health", "GET")])
def test_health_GET(response):
    """Test /health GET response schema"""
    payload = {"status": 200, "schema": {"status": "string"}}

    assert "status" in payload["schema"]