import pytest
@pytest.mark.asyncio
async def test_booking_endpoint_requires_auth(client):
    response = await client.get("/api/bookings")
    assert response.status_code == 401
