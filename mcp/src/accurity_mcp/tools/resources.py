"""Dynamic registration of search + get-by-ID tools for every Accurity resource type."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP

    from accurity_mcp.client import AccurityClient

# ---------------------------------------------------------------------------
# Resource registry
# Each entry: (tool_key, api_path, human_name)
#   tool_key  – used in tool names:  search_<key>  /  get_<key>_by_id
#   api_path  – the Accurity REST path segment: /api/<api_path>/search
#   human_name – used in tool descriptions
# ---------------------------------------------------------------------------
RESOURCES: list[tuple[str, str, str]] = [
    ("attribute", "attribute", "Attribute"),
    ("attribute_definition", "attribute-definition", "Attribute Definition"),
    ("business_model_mapping", "business-model-mapping", "Business Model Mapping"),
    ("business_rule", "business-rule", "Business Rule"),
    ("business_term", "business-term", "Business Term"),
    ("composite_type", "composite-type", "Composite Type"),
    ("custom_property", "custom-property", "Custom Property"),
    ("custom_property_group", "custom-property-group", "Custom Property Group"),
    ("data_asset", "data-asset", "Data Asset"),
    ("data_field", "data-field", "Data Field"),
    ("data_set", "data-set", "Data Set"),
    ("data_source", "data-source", "Data Source"),
    ("data_structure", "data-structure", "Data Structure"),
    ("domain", "domain", "Domain"),
    ("entity", "entity", "Entity"),
    ("process", "process", "Process"),
    ("process_mapping", "process-mapping", "Process Mapping"),
    ("process_step", "process-step", "Process Step"),
    ("requirement", "requirement", "Requirement"),
    ("status_value", "status", "Status Value"),
    ("technical_data_mapping", "technical-data-mapping", "Technical Data Mapping"),
    ("value_type", "value-type", "Value Type"),
]


def _make_search_tool(api_path: str, human_name: str, client: AccurityClient):
    """Return an async function that searches *api_path* resources by name."""

    async def _tool(
        query: str = "",
        start_from: int = 0,
        max_results: int = 20,
    ) -> str:
        try:
            result = await client.search(api_path, query, start_from, max_results)
            return json.dumps(result)
        except Exception as exc:
            return json.dumps({"error": str(exc)})

    _tool.__doc__ = (
        f"Search {human_name} objects in the Accurity data catalog.\n\n"
        f"Args:\n"
        f"  query: Name filter (case-insensitive substring). Leave empty to list all.\n"
        f"  start_from: Pagination offset (default 0).\n"
        f"  max_results: Maximum items to return, 1–100 (default 20).\n\n"
        f"Returns JSON with 'totalCount' and 'items' array."
    )
    return _tool


def _make_get_tool(api_path: str, human_name: str, client: AccurityClient):
    """Return an async function that fetches a single *api_path* resource by ID."""

    async def _tool(id: int) -> str:
        try:
            result = await client.get_by_id(api_path, id)
            return json.dumps(result)
        except Exception as exc:
            return json.dumps({"error": str(exc)})

    _tool.__doc__ = (
        f"Retrieve a single {human_name} object from the Accurity data catalog by its "
        f"integer ID.\n\n"
        f"Args:\n"
        f"  id: The numeric ID of the {human_name}.\n\n"
        f"Returns the full JSON representation of the object."
    )
    return _tool


def register_all_tools(mcp: FastMCP, client: AccurityClient) -> None:
    """Register search and get-by-ID tools for all 22 Accurity resource types."""
    for key, api_path, human_name in RESOURCES:
        search_fn = _make_search_tool(api_path, human_name, client)
        search_fn.__name__ = f"search_{key}"

        get_fn = _make_get_tool(api_path, human_name, client)
        get_fn.__name__ = f"get_{key}_by_id"

        mcp.add_tool(search_fn, name=f"search_{key}", description=search_fn.__doc__)
        mcp.add_tool(get_fn, name=f"get_{key}_by_id", description=get_fn.__doc__)
