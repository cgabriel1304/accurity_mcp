"""Unit tests for tool registration and tool function behaviour."""

import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from accurity_mcp.tools.resources import (
    RESOURCES,
    _make_get_tool,
    _make_search_tool,
)


@pytest.fixture
def mock_client():
    client = MagicMock()
    client.search = AsyncMock(return_value={"totalCount": 1, "items": [{"id": 1, "name": "Revenue"}]})
    client.get_by_id = AsyncMock(return_value={"id": 1, "name": "Revenue"})
    return client


async def test_search_tool_returns_json(mock_client):
    tool = _make_search_tool("business-term", "Business Term", mock_client)
    result = await tool(query="Revenue")

    data = json.loads(result)
    assert data["totalCount"] == 1
    mock_client.search.assert_awaited_once_with("business-term", "Revenue", 0, 20)


async def test_search_tool_default_args(mock_client):
    tool = _make_search_tool("domain", "Domain", mock_client)
    await tool()

    mock_client.search.assert_awaited_once_with("domain", "", 0, 20)


async def test_search_tool_pagination(mock_client):
    tool = _make_search_tool("data-asset", "Data Asset", mock_client)
    await tool(query="Sales", start_from=20, max_results=5)

    mock_client.search.assert_awaited_once_with("data-asset", "Sales", 20, 5)


async def test_get_tool_returns_json(mock_client):
    tool = _make_get_tool("business-term", "Business Term", mock_client)
    result = await tool(id=42)

    data = json.loads(result)
    assert data["id"] == 1
    mock_client.get_by_id.assert_awaited_once_with("business-term", 42)


async def test_search_tool_surfaces_error_as_json(mock_client):
    mock_client.search = AsyncMock(side_effect=Exception("connection refused"))
    tool = _make_search_tool("business-term", "Business Term", mock_client)

    result = await tool(query="x")
    data = json.loads(result)
    assert "error" in data
    assert "connection refused" in data["error"]


async def test_get_tool_surfaces_error_as_json(mock_client):
    mock_client.get_by_id = AsyncMock(side_effect=Exception("404 not found"))
    tool = _make_get_tool("entity", "Entity", mock_client)

    result = await tool(id=999)
    data = json.loads(result)
    assert "error" in data


def test_all_resources_covered():
    """Every resource must have a non-empty key, api_path, and human_name."""
    assert len(RESOURCES) == 22
    for key, api_path, human_name in RESOURCES:
        assert key and api_path and human_name
        assert "_" not in api_path, f"api_path should use hyphens, got: {api_path!r}"


def test_resource_tool_names_are_unique():
    search_names = {f"search_{key}" for key, _, _ in RESOURCES}
    get_names = {f"get_{key}_by_id" for key, _, _ in RESOURCES}
    assert len(search_names) == 22
    assert len(get_names) == 22
    assert search_names.isdisjoint(get_names)
