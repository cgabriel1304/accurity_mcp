"""Unit tests for AccurityClient — all HTTP calls are mocked with respx."""

import time

import pytest
import respx
from httpx import Response

from accurity_mcp.client import AccurityClient

AUTH_URL = "https://auth.example.com/token"
BASE_URL = "https://app.accurity.ai"

TOKEN_RESPONSE = {
    "access_token": "access-abc",
    "refresh_token": "refresh-xyz",
    "expires_in": 299,
    "refresh_expires_in": 1800,
    "token_type": "Bearer",
}


@pytest.fixture
def env_vars(monkeypatch):
    monkeypatch.setenv("ACCURITY_BASE_URL", BASE_URL)
    monkeypatch.setenv("ACCURITY_AUTH_URL", AUTH_URL)
    monkeypatch.setenv("ACCURITY_USERNAME", "user")
    monkeypatch.setenv("ACCURITY_PASSWORD", "pass")


@pytest.fixture
async def client(env_vars):
    c = AccurityClient()
    yield c
    await c.aclose()


@respx.mock
async def test_fetch_token_on_first_call(client):
    respx.post(AUTH_URL).mock(return_value=Response(200, json=TOKEN_RESPONSE))
    respx.post(f"{BASE_URL}/api/business-term/search").mock(
        return_value=Response(200, json={"totalCount": 0, "items": []})
    )

    await client.search("business-term", "Revenue")

    assert client._access_token == "access-abc"
    assert client._refresh_token == "refresh-xyz"


@respx.mock
async def test_token_reused_within_expiry(client):
    auth_call = respx.post(AUTH_URL).mock(return_value=Response(200, json=TOKEN_RESPONSE))
    respx.post(f"{BASE_URL}/api/business-term/search").mock(
        return_value=Response(200, json={"totalCount": 0, "items": []})
    )

    await client.search("business-term", "A")
    await client.search("business-term", "B")

    # Token endpoint called only once
    assert auth_call.call_count == 1


@respx.mock
async def test_token_refreshed_when_expired(client):
    respx.post(AUTH_URL).mock(return_value=Response(200, json=TOKEN_RESPONSE))
    respx.post(f"{BASE_URL}/api/business-term/search").mock(
        return_value=Response(200, json={"totalCount": 0, "items": []})
    )

    await client.search("business-term", "A")

    # Force expiry
    client._token_expires_at = time.time() - 1

    refresh_response = {**TOKEN_RESPONSE, "access_token": "access-new"}
    refresh_call = respx.post(AUTH_URL).mock(return_value=Response(200, json=refresh_response))

    await client.search("business-term", "B")

    assert refresh_call.call_count == 1
    assert client._access_token == "access-new"


@respx.mock
async def test_refresh_failure_triggers_reauth(client):
    respx.post(AUTH_URL).mock(return_value=Response(200, json=TOKEN_RESPONSE))
    respx.post(f"{BASE_URL}/api/business-term/search").mock(
        return_value=Response(200, json={"totalCount": 0, "items": []})
    )

    await client.search("business-term", "A")
    client._token_expires_at = time.time() - 1
    client._refresh_expires_at = time.time() - 1  # also expired

    fresh_response = {**TOKEN_RESPONSE, "access_token": "access-fresh"}
    reauth_call = respx.post(AUTH_URL).mock(return_value=Response(200, json=fresh_response))

    await client.search("business-term", "B")

    assert reauth_call.call_count == 1
    assert client._access_token == "access-fresh"


@respx.mock
async def test_search_sends_correct_payload(client):
    respx.post(AUTH_URL).mock(return_value=Response(200, json=TOKEN_RESPONSE))
    search_route = respx.post(f"{BASE_URL}/api/business-term/search").mock(
        return_value=Response(200, json={"totalCount": 1, "items": [{"id": 1, "name": "Revenue"}]})
    )

    result = await client.search("business-term", "Revenue", start_from=0, max_results=10)

    payload = search_route.calls[0].request.content
    import json
    body = json.loads(payload)
    assert body["filters"][0]["value"] == "Revenue"
    assert body["maxResults"] == 10
    assert result["totalCount"] == 1


@respx.mock
async def test_search_without_query_omits_filter(client):
    respx.post(AUTH_URL).mock(return_value=Response(200, json=TOKEN_RESPONSE))
    search_route = respx.post(f"{BASE_URL}/api/business-term/search").mock(
        return_value=Response(200, json={"totalCount": 0, "items": []})
    )

    await client.search("business-term", "")

    import json
    body = json.loads(search_route.calls[0].request.content)
    assert "filters" not in body


@respx.mock
async def test_get_by_id(client):
    respx.post(AUTH_URL).mock(return_value=Response(200, json=TOKEN_RESPONSE))
    respx.get(f"{BASE_URL}/api/business-term/42").mock(
        return_value=Response(200, json={"id": 42, "name": "Revenue"})
    )

    result = await client.get_by_id("business-term", 42)

    assert result["id"] == 42
    assert result["name"] == "Revenue"
