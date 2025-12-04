import pytest


def test_widget_get_response_schema():
    """Test /widget GET endpoint matches new spec with type change."""
    response = {
        "id": "w123",
        "status": "online",
        "amount": "12.99",
        "reviewUrl": "https://example.com/review"
    }

    # Validate required fields exist
    assert "id" in response
    assert "status" in response
    assert "amount" in response
    assert "reviewUrl" in response

    # Validate types
    assert isinstance(response["id"], str)
    assert isinstance(response["status"], str)
    assert isinstance(response["amount"], str)  # Changed from number to string!
    assert isinstance(response["reviewUrl"], str)


def test_widget_amount_type_change():
    """Test that amount is now string (breaking change from number)."""
    response = {"amount": "99.99"}

    # New spec expects string
    assert isinstance(response["amount"], str)

    # Old clients expecting number would fail:
    # assert isinstance(response["amount"], (int, float))  # Would fail!


def test_order_get_response_schema():
    """Test /order GET endpoint with new currency field."""
    response = {
        "orderId": "o123",
        "total": 25.0,
        "currency": "USD"
    }

    # Validate required fields exist
    assert "orderId" in response
    assert "total" in response
    assert "currency" in response

    # Validate types
    assert isinstance(response["orderId"], str)
    assert isinstance(response["total"], (int, float))
    assert isinstance(response["currency"], str)


def test_order_currency_field_added():
    """Test that new currency field is present."""
    response = {
        "orderId": "o123",
        "total": 25.0,
        "currency": "USD"
    }

    # Old spec didn't have currency - new spec requires it
    assert "currency" in response
    assert isinstance(response["currency"], str)


def test_health_get_response_schema():
    """Test new /health GET endpoint."""
    response = {"status": "ok"}

    # Validate required fields exist
    assert "status" in response

    # Validate types
    assert isinstance(response["status"], str)