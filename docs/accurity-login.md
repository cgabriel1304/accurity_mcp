# Accurity REST API Guide

The Accurity application can be seamlessly integrated with other applications through its REST API. This guide provides essential information about REST API, Swagger UI usage, and integration with Accurity.

## Understanding REST API

A RESTful API is an architectural style for an application program interface (API) that uses HTTP requests to access and manipulate data. These operations include GET, PUT, POST, and DELETE, which correspond to reading, updating, creating, and deleting resources. By default, all requests to the Accurity application utilize version 3 (v3) of the REST API standard. All data is transmitted and received in JSON format.

### How RESTful APIs Operate

A RESTful API employs specific commands to interact with resources. The state of a resource at any given time is referred to as a resource representation. RESTful APIs leverage existing HTTP methods as defined by the RFC 2616 protocol, including:

- **GET** – Retrieve a resource.
- **PUT** – Update or modify a resource.
- **POST** – Create a new resource or search for an object.
- **DELETE** – Remove a resource.

## Introduction to Swagger

Swagger is an Interface Description Language used to describe RESTful APIs in JSON format. It is accompanied by a suite of open-source tools designed to design, build, document, and consume RESTful web services.

### Swagger UI

Swagger UI enables users to visualize and interact with the API's resources without requiring any implementation logic. It is automatically generated from the API Specification, providing visual documentation that simplifies back-end implementation and client-side consumption. All REST APIs are accessible on a single page.

Swagger UI can be accessed at:

```
http(s)://<APP_HOSTNAME>:<PORT>/swagger-ui.html
```

or via the User Menu by selecting the **About** option and clicking the **REST API** link.

## Obtaining an Access Token

To interact with the REST API and receive responses, a valid Access Token is required. In Accurity, Access Tokens are managed by the authentication server. To obtain a new Access Token, execute the following command:

```bash
curl -d 'client_id=accurity' \
     -d 'username=xxx' \
     -d 'password=xxx' \
     -d 'grant_type=password' \
     'http(s)://<HOSTNAME_AUTH-SERVER>/auth/realms/accurity/protocol/openid-connect/token' \
     | python -m json.tool
```

> **Note:** Access Tokens have a default lifespan of 5 minutes.

### Example Response

```json
{
    "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkzojCav23UPmkoeZhEljwL62kCsqxX2wDUdJxPrj8McfMbn6nCwUdQzf64MIhoL0YuE2PtGSa19rKWuynERDmlpS7Qn_TvLNcZdFC4zgmPa9i-K0FofAmiSo7XMoZ81kFAYd1JGbcGZkme6-gX64RTcdJ6AHoJdRsFaQp0nhKC9Ky4KYbK5179V3ObZToWNjAE9g8w8cygNQNwsqcaDQExBQoJb9EH4rY49Egn5A_Xj2lEjtEQvnnTt9wprIMmC_Y7pbj32Gof4MD7ZDeB1POLZbhdAeQ4xsxmlH3r96ZbbeXtXn08Yhgg",
    "expires_in": 299,
    "refresh_expires_in": 1800,
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwRjYTUzMzciLCJzY29wZSI6ImVtYWlsIHByb2ZpbGUiLCJzaWQiOiIxODdhY2RiZC1lODAzLTRhNmUtOWI2Ny0xOGIwZDRjYTUzMzcifQ.HHrw9O0MCq4cM6Pno1YoZmiEZ-Fi91sgKtBALO5tLv4",
    "token_type": "Bearer",
    "not-before-policy": 1642680486,
    "session_state": "187acdbd-e803-4a6e-9b67-18b0d4ca5337",
    "scope": "email profile"
}
```

### Using the Access Token

Include the token in subsequent requests via the `Authorization` header:

```
-H 'Authorization: Bearer <access_token>'
```

## Modifying the Access Token Lifespan

The default lifespan of an Access Token is set to 5 minutes. To change this setting:

1. Open `http(s)://<HOSTNAME_AUTH-SERVER>/auth` and click **Administration Console**.
2. Log in with username `admin` and password `acc@12345`.
3. Navigate to **Realm Settings** and select the **Token** tab.
4. Adjust the **Access Token Lifespan** to the desired value.
5. Scroll to the bottom of the page and click **Save**.
