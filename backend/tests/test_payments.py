import pytest
@pytest.mark.asyncio
async def test_payment_requires_auth(client):
    response = await client.post("/api/payments/create-order", json={"booking_id": 1})
    assert response.status_code == 401
