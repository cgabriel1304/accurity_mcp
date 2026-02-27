"""Accurity HTTP client with Keycloak OAuth2 token management."""

import asyncio
import os
import time

import httpx


class AccurityClient:
    """Async HTTP client for the Accurity REST API.

    Handles Keycloak OAuth2 token acquisition and transparent refresh.
    Token is fetched lazily on the first request.
    """

    def __init__(self) -> None:
        self.base_url = os.environ["ACCURITY_BASE_URL"].rstrip("/")
        self.auth_url = os.environ["ACCURITY_AUTH_URL"]
        self.username = os.environ["ACCURITY_USERNAME"]
        self.password = os.environ["ACCURITY_PASSWORD"]

        self._access_token: str | None = None
        self._refresh_token: str | None = None
        self._token_expires_at: float = 0.0
        self._refresh_expires_at: float = 0.0
        self._lock = asyncio.Lock()
        self._http = httpx.AsyncClient(timeout=30.0)

    async def aclose(self) -> None:
        await self._http.aclose()

    # ------------------------------------------------------------------
    # Token management
    # ------------------------------------------------------------------

    async def _fetch_token(self) -> None:
        """Authenticate with username/password and store the tokens."""
        response = await self._http.post(
            self.auth_url,
            data={
                "client_id": "accurity",
                "username": self.username,
                "password": self.password,
                "grant_type": "password",
            },
        )
        response.raise_for_status()
        self._store_token_response(response.json())

    async def _refresh_access_token(self) -> None:
        """Obtain a new access token using the stored refresh token.

        Falls back to full re-authentication if the refresh token is rejected.
        """
        response = await self._http.post(
            self.auth_url,
            data={
                "client_id": "accurity",
                "grant_type": "refresh_token",
                "refresh_token": self._refresh_token,
            },
        )
        if response.status_code == 400:
            # Refresh token expired or invalid — start fresh
            await self._fetch_token()
            return
        response.raise_for_status()
        data = response.json()
        # Preserve existing refresh token if a new one is not issued
        if "refresh_token" not in data:
            data["refresh_token"] = self._refresh_token
            data.setdefault("refresh_expires_in", 1800)
        self._store_token_response(data)

    def _store_token_response(self, data: dict) -> None:
        now = time.time()
        self._access_token = data["access_token"]
        self._refresh_token = data["refresh_token"]
        # Apply a 30-second safety buffer so we refresh slightly before expiry
        self._token_expires_at = now + data["expires_in"] - 30
        self._refresh_expires_at = now + data["refresh_expires_in"] - 30

    async def _ensure_token(self) -> str:
        """Return a valid access token, refreshing or re-authenticating as needed."""
        async with self._lock:
            now = time.time()
            if self._access_token is None or now >= self._token_expires_at:
                if self._refresh_token and now < self._refresh_expires_at:
                    await self._refresh_access_token()
                else:
                    await self._fetch_token()
        return self._access_token  # type: ignore[return-value]

    async def _auth_headers(self) -> dict[str, str]:
        token = await self._ensure_token()
        return {"Authorization": f"Bearer {token}"}

    # ------------------------------------------------------------------
    # API operations
    # ------------------------------------------------------------------

    async def search(
        self,
        resource_path: str,
        query: str = "",
        start_from: int = 0,
        max_results: int = 20,
    ) -> dict:
        """Search a resource by name.

        If *query* is empty, all objects are returned (up to *max_results*).
        """
        headers = await self._auth_headers()
        payload: dict = {
            "startFrom": start_from,
            "maxResults": max_results,
            "sort": {"type": "ASCENDING", "property": "name"},
        }
        if query:
            payload["filters"] = [
                {"type": "SIMPLE_QUERY", "property": "name", "value": query}
            ]

        response = await self._http.post(
            f"{self.base_url}/api/{resource_path}/search",
            json=payload,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()

    async def get_by_id(self, resource_path: str, item_id: int) -> dict:
        """Retrieve a single resource object by its integer ID."""
        headers = await self._auth_headers()
        response = await self._http.get(
            f"{self.base_url}/api/{resource_path}/{item_id}",
            headers=headers,
        )
        response.raise_for_status()
        return response.json()
