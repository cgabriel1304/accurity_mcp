# Accurity REST API Reference

**Version:** 1.22.17 (OAS3)  
**Base URL:** `https://app.accurity.ai`  
**API Docs:** `/v3/api-docs/default`

This API provides public access to all Accurity Glossary objects. It follows a consistent CRUD pattern across all resource types and supports both synchronous and asynchronous deletion.

## Authentication

All endpoints require authentication. Include your credentials according to your Accurity deployment configuration.

## Common Patterns

All resource endpoints follow a standard pattern:

| Pattern | Method | Description |
|---------|--------|-------------|
| `PUT /api/{resource}` | PUT | Update an existing object |
| `POST /api/{resource}` | POST | Create a new object |
| `POST /api/{resource}/search` | POST | Search objects with filters |
| `GET /api/{resource}/{id}` | GET | Retrieve an object by ID |
| `DELETE /api/{resource}/{id}` | DELETE | Synchronously delete an object |
| `DELETE /api/{resource}/async/{id}` | DELETE | Asynchronously delete (returns a Job) |

### Search Request Body

The search endpoints accept a JSON body with the following structure:

```json
{
  "startFrom": 0,
  "maxResults": 50,
  "filters": [
    {
      "type": "SIMPLE_QUERY",
      "property": "name",
      "value": "search term",
      "timezone": "UTC",
      "relationType": "RELATED_TO"
    }
  ],
  "sort": {
    "type": "ASCENDING",
    "property": "name"
  },
  "asOfTime": 0
}
```

**Sort types:** `ASCENDING`, `DESCENDING`  
**Filter type:** `SIMPLE_QUERY`  
**Relation types:** `RELATED_TO`

### Common Response Fields

Most resource objects share these common fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer (int64) | Unique identifier |
| `version` | integer | Version for optimistic locking |
| `name` | string | Display name |
| `objectType` | string | Type discriminator |
| `createdDate` | integer (epoch ms) | Creation timestamp |
| `changedDate` | integer (epoch ms) | Last modification timestamp |
| `createdBy` | object | User who created: `{ id, name }` |
| `changedBy` | object | User who last modified: `{ id, name }` |
| `description` | object | `{ plainTextValue, formattedValue }` |
| `tags` | array | Associated tags |
| `chips` | array | Associated chips/badges |
| `customPropertyValues` | object | Map of custom property ID to values |

---

## Table of Contents

- [Asynchronous Job](#asynchronous-job)
  - [PUT /api/job/{id}/stop](#put-api-job-id-stop)
  - [PUT /api/job/{id}/restart](#put-api-job-id-restart)
  - [GET /api/job/{id}](#get-api-job-id)
- [Attribute](#attribute)
  - [PUT /api/attribute](#put-api-attribute)
  - [POST /api/attribute](#post-api-attribute)
  - [POST /api/attribute/search](#post-api-attribute-search)
  - [GET /api/attribute/{id}](#get-api-attribute-id)
  - [DELETE /api/attribute/{id}](#delete-api-attribute-id)
  - [DELETE /api/attribute/async/{id}](#delete-api-attribute-async-id)
- [Attribute Definition](#attribute-definition)
  - [PUT /api/attribute-definition](#put-api-attribute-definition)
  - [POST /api/attribute-definition](#post-api-attribute-definition)
  - [POST /api/attribute-definition/search](#post-api-attribute-definition-search)
  - [GET /api/attribute-definition/{id}](#get-api-attribute-definition-id)
  - [DELETE /api/attribute-definition/{id}](#delete-api-attribute-definition-id)
  - [DELETE /api/attribute-definition/async/{id}](#delete-api-attribute-definition-async-id)
- [Business Model Mapping](#business-model-mapping)
  - [PUT /api/business-model-mapping](#put-api-business-model-mapping)
  - [POST /api/business-model-mapping](#post-api-business-model-mapping)
  - [POST /api/business-model-mapping/search](#post-api-business-model-mapping-search)
  - [GET /api/business-model-mapping/{id}](#get-api-business-model-mapping-id)
  - [DELETE /api/business-model-mapping/{id}](#delete-api-business-model-mapping-id)
  - [DELETE /api/business-model-mapping/async/{id}](#delete-api-business-model-mapping-async-id)
- [Business Rule](#business-rule)
  - [PUT /api/business-rule](#put-api-business-rule)
  - [POST /api/business-rule](#post-api-business-rule)
  - [POST /api/business-rule/search](#post-api-business-rule-search)
  - [GET /api/business-rule/{id}](#get-api-business-rule-id)
  - [DELETE /api/business-rule/{id}](#delete-api-business-rule-id)
  - [DELETE /api/business-rule/async/{id}](#delete-api-business-rule-async-id)
- [Business Term](#business-term)
  - [PUT /api/business-term](#put-api-business-term)
  - [POST /api/business-term](#post-api-business-term)
  - [POST /api/business-term/search](#post-api-business-term-search)
  - [GET /api/business-term/{id}](#get-api-business-term-id)
  - [DELETE /api/business-term/{id}](#delete-api-business-term-id)
  - [DELETE /api/business-term/async/{id}](#delete-api-business-term-async-id)
- [Composite Type](#composite-type)
  - [PUT /api/composite-type](#put-api-composite-type)
  - [POST /api/composite-type](#post-api-composite-type)
  - [POST /api/composite-type/search](#post-api-composite-type-search)
  - [GET /api/composite-type/{id}](#get-api-composite-type-id)
  - [DELETE /api/composite-type/{id}](#delete-api-composite-type-id)
  - [DELETE /api/composite-type/async/{id}](#delete-api-composite-type-async-id)
- [Custom Property](#custom-property)
  - [PUT /api/custom-property](#put-api-custom-property)
  - [POST /api/custom-property](#post-api-custom-property)
  - [POST /api/custom-property/search](#post-api-custom-property-search)
  - [GET /api/custom-property/{id}](#get-api-custom-property-id)
  - [DELETE /api/custom-property/{id}](#delete-api-custom-property-id)
  - [DELETE /api/custom-property/async/{id}](#delete-api-custom-property-async-id)
- [Custom Property Group](#custom-property-group)
  - [PUT /api/custom-property-group](#put-api-custom-property-group)
  - [POST /api/custom-property-group](#post-api-custom-property-group)
  - [POST /api/custom-property-group/search](#post-api-custom-property-group-search)
  - [GET /api/custom-property-group/{id}](#get-api-custom-property-group-id)
  - [DELETE /api/custom-property-group/{id}](#delete-api-custom-property-group-id)
  - [DELETE /api/custom-property-group/async/{id}](#delete-api-custom-property-group-async-id)
- [Data Asset](#data-asset)
  - [PUT /api/data-asset](#put-api-data-asset)
  - [POST /api/data-asset](#post-api-data-asset)
  - [POST /api/data-asset/search](#post-api-data-asset-search)
  - [GET /api/data-asset/{id}](#get-api-data-asset-id)
  - [DELETE /api/data-asset/{id}](#delete-api-data-asset-id)
  - [DELETE /api/data-asset/async/{id}](#delete-api-data-asset-async-id)
- [Data Field](#data-field)
  - [PUT /api/data-field](#put-api-data-field)
  - [POST /api/data-field](#post-api-data-field)
  - [POST /api/data-field/{id}/profile](#post-api-data-field-id-profile)
  - [POST /api/data-field/search](#post-api-data-field-search)
  - [GET /api/data-field/{id}](#get-api-data-field-id)
  - [DELETE /api/data-field/{id}](#delete-api-data-field-id)
  - [DELETE /api/data-field/async/{id}](#delete-api-data-field-async-id)
- [Data Set](#data-set)
  - [PUT /api/data-set](#put-api-data-set)
  - [POST /api/data-set](#post-api-data-set)
  - [POST /api/data-set/search](#post-api-data-set-search)
  - [GET /api/data-set/{id}](#get-api-data-set-id)
  - [DELETE /api/data-set/{id}](#delete-api-data-set-id)
  - [GET /api/data-set/sync/{dataSetId}/{scanUuid}](#get-api-data-set-sync-dataSetId-scanUuid)
  - [DELETE /api/data-set/async/{id}](#delete-api-data-set-async-id)
- [Data Source](#data-source)
  - [PUT /api/data-source](#put-api-data-source)
  - [POST /api/data-source](#post-api-data-source)
  - [POST /api/data-source/search](#post-api-data-source-search)
  - [GET /api/data-source/{id}](#get-api-data-source-id)
  - [DELETE /api/data-source/{id}](#delete-api-data-source-id)
  - [DELETE /api/data-source/async/{id}](#delete-api-data-source-async-id)
- [Data Structure](#data-structure)
  - [PUT /api/data-structure](#put-api-data-structure)
  - [POST /api/data-structure](#post-api-data-structure)
  - [POST /api/data-structure/search](#post-api-data-structure-search)
  - [GET /api/data-structure/{id}](#get-api-data-structure-id)
  - [DELETE /api/data-structure/{id}](#delete-api-data-structure-id)
  - [DELETE /api/data-structure/async/{id}](#delete-api-data-structure-async-id)
- [Domain](#domain)
  - [PUT /api/domain](#put-api-domain)
  - [POST /api/domain](#post-api-domain)
  - [POST /api/domain/search](#post-api-domain-search)
  - [GET /api/domain/{id}](#get-api-domain-id)
  - [DELETE /api/domain/{id}](#delete-api-domain-id)
  - [DELETE /api/domain/async/{id}](#delete-api-domain-async-id)
- [Entity](#entity)
  - [PUT /api/entity](#put-api-entity)
  - [POST /api/entity](#post-api-entity)
  - [POST /api/entity/search](#post-api-entity-search)
  - [GET /api/entity/{id}](#get-api-entity-id)
  - [DELETE /api/entity/{id}](#delete-api-entity-id)
  - [DELETE /api/entity/async/{id}](#delete-api-entity-async-id)
- [Process](#process)
  - [PUT /api/process](#put-api-process)
  - [POST /api/process](#post-api-process)
  - [POST /api/process/search](#post-api-process-search)
  - [GET /api/process/{id}](#get-api-process-id)
  - [DELETE /api/process/{id}](#delete-api-process-id)
  - [DELETE /api/process/async/{id}](#delete-api-process-async-id)
- [Process Mapping](#process-mapping)
  - [PUT /api/process-mapping](#put-api-process-mapping)
  - [POST /api/process-mapping](#post-api-process-mapping)
  - [POST /api/process-mapping/search](#post-api-process-mapping-search)
  - [GET /api/process-mapping/{id}](#get-api-process-mapping-id)
  - [DELETE /api/process-mapping/{id}](#delete-api-process-mapping-id)
  - [DELETE /api/process-mapping/async/{id}](#delete-api-process-mapping-async-id)
- [Process Step](#process-step)
  - [PUT /api/process-step](#put-api-process-step)
  - [POST /api/process-step](#post-api-process-step)
  - [POST /api/process-step/search](#post-api-process-step-search)
  - [GET /api/process-step/{id}](#get-api-process-step-id)
  - [DELETE /api/process-step/{id}](#delete-api-process-step-id)
  - [DELETE /api/process-step/async/{id}](#delete-api-process-step-async-id)
- [Requirement](#requirement)
  - [PUT /api/requirement](#put-api-requirement)
  - [POST /api/requirement](#post-api-requirement)
  - [POST /api/requirement/search](#post-api-requirement-search)
  - [GET /api/requirement/{id}](#get-api-requirement-id)
  - [DELETE /api/requirement/{id}](#delete-api-requirement-id)
  - [DELETE /api/requirement/async/{id}](#delete-api-requirement-async-id)
- [Status Value](#status-value)
  - [PUT /api/status](#put-api-status)
  - [POST /api/status](#post-api-status)
  - [POST /api/status/search](#post-api-status-search)
  - [GET /api/status/{id}](#get-api-status-id)
  - [DELETE /api/status/{id}](#delete-api-status-id)
  - [DELETE /api/status/async/{id}](#delete-api-status-async-id)
- [Technical Data Mapping](#technical-data-mapping)
  - [PUT /api/technical-data-mapping](#put-api-technical-data-mapping)
  - [POST /api/technical-data-mapping](#post-api-technical-data-mapping)
  - [POST /api/technical-data-mapping/search](#post-api-technical-data-mapping-search)
  - [GET /api/technical-data-mapping/{id}](#get-api-technical-data-mapping-id)
  - [DELETE /api/technical-data-mapping/{id}](#delete-api-technical-data-mapping-id)
  - [DELETE /api/technical-data-mapping/async/{id}](#delete-api-technical-data-mapping-async-id)
- [Value Type](#value-type)
  - [PUT /api/value-type](#put-api-value-type)
  - [POST /api/value-type](#post-api-value-type)
  - [POST /api/value-type/search](#post-api-value-type-search)
  - [GET /api/value-type/{id}](#get-api-value-type-id)
  - [DELETE /api/value-type/{id}](#delete-api-value-type-id)
  - [DELETE /api/value-type/async/{id}](#delete-api-value-type-async-id)

---

## Asynchronous Job

Manage asynchronous background jobs. When deleting resources asynchronously, a job ID is returned that can be tracked using these endpoints.

### `PUT` /api/job/{id}/stop

**Stop a running asynchronous job**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "status": "COMPLETED",
  "startTime": "2026-02-26T04:37:55.880Z",
  "endTime": "2026-02-26T04:37:55.880Z"
}
```

---

### `PUT` /api/job/{id}/restart

**Restart a stopped asynchronous job**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "status": "COMPLETED",
  "startTime": "2026-02-26T04:37:55.885Z",
  "endTime": "2026-02-26T04:37:55.885Z"
}
```

---

### `GET` /api/job/{id}

**Get status and details of an asynchronous job**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "status": "COMPLETED",
  "startTime": "2026-02-26T04:37:55.889Z",
  "endTime": "2026-02-26T04:37:55.889Z"
}
```

---

## Attribute

Manage Attribute objects — typed properties attached to Entities in the Business Glossary.

### `PUT` /api/attribute

**Update Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "descriptionInherited": true,
  "entity": {
    "id": 0,
    "version": 0,
    "name": "string",
    "objectType": "string",
    "createdDate": 0,
    "changedDate": 0,
    "createdBy": {
      "id": 0,
      "name": "string"
    },
    "changedBy": {
      "id": 0,
      "name": "string"
    },
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "chips": [
      {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    ],
    "tags": [
      {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    ],
    "basedOnBusinessTerm": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "status": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "entityType": "Main",
    "parent": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "customPropertyValues": {
      "1": [
        "string"
      ],
      "2": [
        "string"
      ]
    },
    "childrenCounts": {
      "id": 0,
      "type": "string",
      "domainsCount": 0,

  // ... (truncated for brevity)
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "descriptionInherited": true,
  "entity": {
    "id": 0,
    "version": 0,
    "name": "string",
    "objectType": "string",
    "createdDate": 0,
    "changedDate": 0,
    "createdBy": {
      "id": 0,
      "name": "string"
    },
    "changedBy": {
      "id": 0,
      "name": "string"
    },
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "chips": [
      {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    ],
    "tags": [
      {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    ],
    "basedOnBusinessTerm": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "status": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "entityType": "Main",
    "parent": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "customPropertyValues": {
      "1": [
        "string"
      ],
      "2": [
        "string"
      ]
    },
    "childrenCounts": {
      "id": 0,
      "type": "string",
      "domainsCount": 0,

  // ... (truncated for brevity)
```

---

### `POST` /api/attribute

**Create Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "descriptionInherited": true,
  "entity": {
    "id": 0,
    "version": 0,
    "name": "string",
    "objectType": "string",
    "createdDate": 0,
    "changedDate": 0,
    "createdBy": {
      "id": 0,
      "name": "string"
    },
    "changedBy": {
      "id": 0,
      "name": "string"
    },
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "chips": [
      {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    ],
    "tags": [
      {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    ],
    "basedOnBusinessTerm": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "status": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "entityType": "Main",
    "parent": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "customPropertyValues": {
      "1": [
        "string"
      ],
      "2": [
        "string"
      ]
    },
    "childrenCounts": {
      "id": 0,
      "type": "string",
      "domainsCount": 0,

  // ... (truncated for brevity)
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "descriptionInherited": true,
  "entity": {
    "id": 0,
    "version": 0,
    "name": "string",
    "objectType": "string",
    "createdDate": 0,
    "changedDate": 0,
    "createdBy": {
      "id": 0,
      "name": "string"
    },
    "changedBy": {
      "id": 0,
      "name": "string"
    },
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "chips": [
      {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    ],
    "tags": [
      {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    ],
    "basedOnBusinessTerm": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "status": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "entityType": "Main",
    "parent": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "customPropertyValues": {
      "1": [
        "string"
      ],
      "2": [
        "string"
      ]
    },
    "childrenCounts": {
      "id": 0,
      "type": "string",
      "domainsCount": 0,

  // ... (truncated for brevity)
```

---

### `POST` /api/attribute/search

**Search Objects**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "startFrom": 0,
  "maxResults": 0,
  "filters": [
    {
      "type": "SIMPLE_QUERY",
      "property": "string",
      "value": "string",
      "timezone": "string",
      "relationType": "RELATED_TO"
    }
  ],
  "sort": {
    "type": "ASCENDING",
    "property": "string"
  },
  "asOfTime": 0
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "size": 0,
  "rows": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
      "changedBy": {
        "id": 0,
        "name": "string"
      },
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "chips": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "tags": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "descriptionInherited": true,
      "entity": {
        "id": 0,
        "version": 0,
        "name": "string",
        "objectType": "string",
        "createdDate": 0,
        "changedDate": 0,
        "createdBy": {
          "id": 0,
          "name": "string"
        },
        "changedBy": {
          "id": 0,
          "name": "string"
        },
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "chips": [
          {
            "id": 0,
            "name": "string",
            "description": {
              "plainTextValue": "string",
              "formattedValue": "string"
            },
            "objectType": "string"
          }
        ],
        "tags": [
          {
            "id": 0,
            "name": "string",
            "description": {
              "plainTextValue": "string",
              "formattedValue": "string"
            },
            "objectType": "string"
          }
        ],
        "basedOnBusinessTerm": {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        },
        "status": {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        },
        "e
  // ... (truncated for brevity)
```

---

### `GET` /api/attribute/{id}

**Find Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "descriptionInherited": true,
  "entity": {
    "id": 0,
    "version": 0,
    "name": "string",
    "objectType": "string",
    "createdDate": 0,
    "changedDate": 0,
    "createdBy": {
      "id": 0,
      "name": "string"
    },
    "changedBy": {
      "id": 0,
      "name": "string"
    },
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "chips": [
      {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    ],
    "tags": [
      {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    ],
    "basedOnBusinessTerm": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "status": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "entityType": "Main",
    "parent": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "customPropertyValues": {
      "1": [
        "string"
      ],
      "2": [
        "string"
      ]
    },
    "childrenCounts": {
      "id": 0,
      "type": "string",
      "domainsCount": 0,

  // ... (truncated for brevity)
```

---

### `DELETE` /api/attribute/{id}

**Delete Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `DELETE` /api/attribute/async/{id}

**Delete an object asynchronously (returns a Job ID)**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example** (Asynchronous Job)

```json
{
  "id": 0,
  "status": "COMPLETED",
  "startTime": "2026-02-26T04:37:55.977Z",
  "endTime": "2026-02-26T04:37:55.977Z"
}
```

---

## Attribute Definition

Manage Attribute Definition objects — templates that define the structure and type of Attributes.

### `PUT` /api/attribute-definition

**Update Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "basedOnBusinessTerm": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "parent": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "compositeTypeComponent": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "attributeDefinitionType": "Composite",
  "compositeType": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "targetEntity": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "valueType": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
   
  // ... (truncated for brevity)
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "basedOnBusinessTerm": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "parent": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "compositeTypeComponent": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "attributeDefinitionType": "Composite",
  "compositeType": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "targetEntity": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "valueType": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
   
  // ... (truncated for brevity)
```

---

### `POST` /api/attribute-definition

**Create Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "basedOnBusinessTerm": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "parent": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "compositeTypeComponent": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "attributeDefinitionType": "Composite",
  "compositeType": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "targetEntity": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "valueType": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
   
  // ... (truncated for brevity)
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "basedOnBusinessTerm": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "parent": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "compositeTypeComponent": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "attributeDefinitionType": "Composite",
  "compositeType": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "targetEntity": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "valueType": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
   
  // ... (truncated for brevity)
```

---

### `POST` /api/attribute-definition/search

**Search Objects**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "startFrom": 0,
  "maxResults": 0,
  "filters": [
    {
      "type": "SIMPLE_QUERY",
      "property": "string",
      "value": "string",
      "timezone": "string",
      "relationType": "RELATED_TO"
    }
  ],
  "sort": {
    "type": "ASCENDING",
    "property": "string"
  },
  "asOfTime": 0
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "size": 0,
  "rows": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
      "changedBy": {
        "id": 0,
        "name": "string"
      },
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "chips": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "tags": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "basedOnBusinessTerm": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "parent": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "compositeTypeComponent": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "status": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "attributeDefinitionType": "Composite",
      "compositeType": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "targetEntity": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "valueType": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
   
  // ... (truncated for brevity)
```

---

### `GET` /api/attribute-definition/{id}

**Find Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "basedOnBusinessTerm": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "parent": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "compositeTypeComponent": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "attributeDefinitionType": "Composite",
  "compositeType": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "targetEntity": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "valueType": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
   
  // ... (truncated for brevity)
```

---

### `DELETE` /api/attribute-definition/{id}

**Delete Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `DELETE` /api/attribute-definition/async/{id}

**Delete an object asynchronously (returns a Job ID)**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example** (Asynchronous Job)

```json
{
  "id": 0,
  "status": "COMPLETED",
  "startTime": "2026-02-26T04:37:56.040Z",
  "endTime": "2026-02-26T04:37:56.040Z"
}
```

---

## Business Model Mapping

Manage Business Model Mapping objects — mappings between business model elements.

### `PUT` /api/business-model-mapping

**Update Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "baseDataSet": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string",
    "dataSetType": "Logical",
    "dataSetDomains": [
      {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    ],
    "dataSource": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSourceType": "ACCURITY_EDGE_PULL"
    }
  },
  "businessModelMappingType": "Entity",
  "baseEntity": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "baseAttributeDefinition": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "baseAttribute": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "baseDataStructure": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "baseDataField": {
  // ... (truncated for brevity)
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "baseDataSet": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string",
    "dataSetType": "Logical",
    "dataSetDomains": [
      {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    ],
    "dataSource": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSourceType": "ACCURITY_EDGE_PULL"
    }
  },
  "businessModelMappingType": "Entity",
  "baseEntity": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "baseAttributeDefinition": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "baseAttribute": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "baseDataStructure": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "baseDataField": {
  // ... (truncated for brevity)
```

---

### `POST` /api/business-model-mapping

**Create Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "baseDataSet": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string",
    "dataSetType": "Logical",
    "dataSetDomains": [
      {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    ],
    "dataSource": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSourceType": "ACCURITY_EDGE_PULL"
    }
  },
  "businessModelMappingType": "Entity",
  "baseEntity": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "baseAttributeDefinition": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "baseAttribute": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "baseDataStructure": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "baseDataField": {
  // ... (truncated for brevity)
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "baseDataSet": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string",
    "dataSetType": "Logical",
    "dataSetDomains": [
      {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    ],
    "dataSource": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSourceType": "ACCURITY_EDGE_PULL"
    }
  },
  "businessModelMappingType": "Entity",
  "baseEntity": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "baseAttributeDefinition": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "baseAttribute": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "baseDataStructure": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "baseDataField": {
  // ... (truncated for brevity)
```

---

### `POST` /api/business-model-mapping/search

**Search Objects**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "startFrom": 0,
  "maxResults": 0,
  "filters": [
    {
      "type": "SIMPLE_QUERY",
      "property": "string",
      "value": "string",
      "timezone": "string",
      "relationType": "RELATED_TO"
    }
  ],
  "sort": {
    "type": "ASCENDING",
    "property": "string"
  },
  "asOfTime": 0
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "size": 0,
  "rows": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
      "changedBy": {
        "id": 0,
        "name": "string"
      },
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "chips": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "tags": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "status": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "baseDataSet": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string",
        "dataSetType": "Logical",
        "dataSetDomains": [
          {
            "id": 0,
            "name": "string",
            "description": {
              "plainTextValue": "string",
              "formattedValue": "string"
            },
            "objectType": "string"
          }
        ],
        "dataSource": {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string",
          "dataSourceType": "ACCURITY_EDGE_PULL"
        }
      },
      "businessModelMappingType": "Entity",
      "baseEntity": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "baseAttributeDefinition": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType":
  // ... (truncated for brevity)
```

---

### `GET` /api/business-model-mapping/{id}

**Find Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "baseDataSet": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string",
    "dataSetType": "Logical",
    "dataSetDomains": [
      {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    ],
    "dataSource": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSourceType": "ACCURITY_EDGE_PULL"
    }
  },
  "businessModelMappingType": "Entity",
  "baseEntity": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "baseAttributeDefinition": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "baseAttribute": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "baseDataStructure": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "baseDataField": {
  // ... (truncated for brevity)
```

---

### `DELETE` /api/business-model-mapping/{id}

**Delete Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `DELETE` /api/business-model-mapping/async/{id}

**Delete an object asynchronously (returns a Job ID)**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example** (Asynchronous Job)

```json
{
  "id": 0,
  "status": "COMPLETED",
  "startTime": "2026-02-26T04:37:56.130Z",
  "endTime": "2026-02-26T04:37:56.130Z"
}
```

---

## Business Rule

Manage Business Rule objects — formal rules governing business data and processes.

### `PUT` /api/business-rule

**Update Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "definition": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "dimension": "Accuracy",
  "threshold": "string",
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "definition": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "dimension": "Accuracy",
  "threshold": "string",
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

---

### `POST` /api/business-rule

**Create Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "definition": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "dimension": "Accuracy",
  "threshold": "string",
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "definition": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "dimension": "Accuracy",
  "threshold": "string",
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

---

### `POST` /api/business-rule/search

**Search Objects**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "startFrom": 0,
  "maxResults": 0,
  "filters": [
    {
      "type": "SIMPLE_QUERY",
      "property": "string",
      "value": "string",
      "timezone": "string",
      "relationType": "RELATED_TO"
    }
  ],
  "sort": {
    "type": "ASCENDING",
    "property": "string"
  },
  "asOfTime": 0
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "size": 0,
  "rows": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
      "changedBy": {
        "id": 0,
        "name": "string"
      },
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "chips": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "tags": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "status": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "definition": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "dimension": "Accuracy",
      "threshold": "string",
      "customPropertyValues": {
        "1": [
          "string"
        ],
        "2": [
          "string"
        ]
      },
      "childrenCounts": {
        "id": 0,
        "type": "string",
        "domainsCount": 0,
        "domainOwnersCount": 0,
        "dataStewardsCount": 0,
        "dataAssetsCount": 0,
        "dataSetsCount": 0,
        "dataStructuresCount": 0,
        "dataFieldsCount": 0,
        "businessTermsCount": 0,
        "entitiesCount": 0,
        "referenceAttributeTargetEntitiesCount": 0,
        "attributesCount": 0,
        "calculationRulesCount": 0,
        "attributeDefinitionsCount": 0,
        "compositeTypesCount": 0,
        "customPropertiesCount": 0,
        "businessRulesCount": 0,
        "businessModelMappingsCount": 0,
        "processesCount": 0,
        "processStepsCount": 0,
        "processMappingsCount": 0,
        "technicalDataMappingsCount": 0,
        "commentsCount": 0,
        "objectType": "string"
      },
      "activeNotifications": {
        "COMMENT_UPDATE": true,
        "OBJECT_UPDATE": true
      }
    }
  ],
  "existingObjects": 0,
  "
  // ... (truncated for brevity)
```

---

### `GET` /api/business-rule/{id}

**Find Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "definition": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "dimension": "Accuracy",
  "threshold": "string",
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

---

### `DELETE` /api/business-rule/{id}

**Delete Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `DELETE` /api/business-rule/async/{id}

**Delete an object asynchronously (returns a Job ID)**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example** (Asynchronous Job)

```json
{
  "id": 0,
  "status": "COMPLETED",
  "startTime": "2026-02-26T04:37:56.192Z",
  "endTime": "2026-02-26T04:37:56.192Z"
}
```

---

## Business Term

Manage Business Term objects — the core glossary entries that define business concepts.

### `PUT` /api/business-term

**Update Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "synonym": "string",
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "domain": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "relatedBusinessTerms": [
    {
      "id": 0,
      "relationType": "Relates to",
      "parent": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "relatedBusinessTerm": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    }
  ],
  "referencedBy": [
    {
      "id": 0,
      "relationType": "Relates to",
      "parent": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "relatedBusinessTerm": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    }
  ],
  "relatedValues": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
  // ... (truncated for brevity)
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "synonym": "string",
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "domain": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "relatedBusinessTerms": [
    {
      "id": 0,
      "relationType": "Relates to",
      "parent": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "relatedBusinessTerm": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    }
  ],
  "referencedBy": [
    {
      "id": 0,
      "relationType": "Relates to",
      "parent": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "relatedBusinessTerm": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    }
  ],
  "relatedValues": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
  // ... (truncated for brevity)
```

---

### `POST` /api/business-term

**Create Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "synonym": "string",
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "domain": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "relatedBusinessTerms": [
    {
      "id": 0,
      "relationType": "Relates to",
      "parent": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "relatedBusinessTerm": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    }
  ],
  "referencedBy": [
    {
      "id": 0,
      "relationType": "Relates to",
      "parent": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "relatedBusinessTerm": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    }
  ],
  "relatedValues": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
  // ... (truncated for brevity)
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "synonym": "string",
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "domain": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "relatedBusinessTerms": [
    {
      "id": 0,
      "relationType": "Relates to",
      "parent": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "relatedBusinessTerm": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    }
  ],
  "referencedBy": [
    {
      "id": 0,
      "relationType": "Relates to",
      "parent": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "relatedBusinessTerm": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    }
  ],
  "relatedValues": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
  // ... (truncated for brevity)
```

---

### `POST` /api/business-term/search

**Search Objects**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "startFrom": 0,
  "maxResults": 0,
  "filters": [
    {
      "type": "SIMPLE_QUERY",
      "property": "string",
      "value": "string",
      "timezone": "string",
      "relationType": "RELATED_TO"
    }
  ],
  "sort": {
    "type": "ASCENDING",
    "property": "string"
  },
  "asOfTime": 0
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "size": 0,
  "rows": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
      "changedBy": {
        "id": 0,
        "name": "string"
      },
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "chips": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "tags": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "synonym": "string",
      "status": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "domain": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "relatedBusinessTerms": [
        {
          "id": 0,
          "relationType": "Relates to",
          "parent": {
            "id": 0,
            "name": "string",
            "description": {
              "plainTextValue": "string",
              "formattedValue": "string"
            },
            "objectType": "string"
          },
          "relatedBusinessTerm": {
            "id": 0,
            "name": "string",
            "description": {
              "plainTextValue": "string",
              "formattedValue": "string"
            },
            "objectType": "string"
          }
        }
      ],
      "referencedBy": [
        {
          "id": 0,
          "relationType": "Relates to",
          "parent": {
            "id": 0,
            "name": "string",
            "description": {
              "plainTextValue": "string",
              "formattedValue": "string"
            },
            "objectType": "string"
          },
          "relatedBusinessTerm": {
            "id": 0,
            "nam
  // ... (truncated for brevity)
```

---

### `GET` /api/business-term/{id}

**Find Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "synonym": "string",
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "domain": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "relatedBusinessTerms": [
    {
      "id": 0,
      "relationType": "Relates to",
      "parent": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "relatedBusinessTerm": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    }
  ],
  "referencedBy": [
    {
      "id": 0,
      "relationType": "Relates to",
      "parent": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "relatedBusinessTerm": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    }
  ],
  "relatedValues": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
  // ... (truncated for brevity)
```

---

### `DELETE` /api/business-term/{id}

**Delete Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `DELETE` /api/business-term/async/{id}

**Delete an object asynchronously (returns a Job ID)**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example** (Asynchronous Job)

```json
{
  "id": 0,
  "status": "COMPLETED",
  "startTime": "2026-02-26T04:37:56.260Z",
  "endTime": "2026-02-26T04:37:56.260Z"
}
```

---

## Composite Type

Manage Composite Type objects — complex data types composed of multiple fields.

### `PUT` /api/composite-type

**Update Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "components": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
      "changedBy": {
        "id": 0,
        "name": "string"
      },
      "componentType": "Value",
      "valueType": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "targetEntity": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    }
  ],
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 
  // ... (truncated for brevity)
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "components": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
      "changedBy": {
        "id": 0,
        "name": "string"
      },
      "componentType": "Value",
      "valueType": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "targetEntity": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    }
  ],
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 
  // ... (truncated for brevity)
```

---

### `POST` /api/composite-type

**Create Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "components": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
      "changedBy": {
        "id": 0,
        "name": "string"
      },
      "componentType": "Value",
      "valueType": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "targetEntity": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    }
  ],
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 
  // ... (truncated for brevity)
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "components": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
      "changedBy": {
        "id": 0,
        "name": "string"
      },
      "componentType": "Value",
      "valueType": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "targetEntity": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    }
  ],
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 
  // ... (truncated for brevity)
```

---

### `POST` /api/composite-type/search

**Search Objects**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "startFrom": 0,
  "maxResults": 0,
  "filters": [
    {
      "type": "SIMPLE_QUERY",
      "property": "string",
      "value": "string",
      "timezone": "string",
      "relationType": "RELATED_TO"
    }
  ],
  "sort": {
    "type": "ASCENDING",
    "property": "string"
  },
  "asOfTime": 0
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "size": 0,
  "rows": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
      "changedBy": {
        "id": 0,
        "name": "string"
      },
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "chips": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "tags": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "status": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "components": [
        {
          "id": 0,
          "version": 0,
          "name": "string",
          "objectType": "string",
          "createdDate": 0,
          "changedDate": 0,
          "createdBy": {
            "id": 0,
            "name": "string"
          },
          "changedBy": {
            "id": 0,
            "name": "string"
          },
          "componentType": "Value",
          "valueType": {
            "id": 0,
            "name": "string",
            "description": {
              "plainTextValue": "string",
              "formattedValue": "string"
            },
            "objectType": "string"
          },
          "targetEntity": {
            "id": 0,
            "name": "string",
            "description": {
              "plainTextValue": "string",
              "formattedValue": "string"
            },
            "objectType": "string"
          }
        }
      ],
      "customPropertyValues": {
        "1": [
          "string"
        ],
        "2": [
          "string"
        ]
      },
      "childrenCounts": {
        "id": 0,
        "type": "string",
        "domainsCount": 0,
        "domainOwnersCount": 0,
        "dataStewardsCount": 0,
        "dataAssetsCount": 0,
        "dataSetsCount": 0,

  // ... (truncated for brevity)
```

---

### `GET` /api/composite-type/{id}

**Find Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "components": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
      "changedBy": {
        "id": 0,
        "name": "string"
      },
      "componentType": "Value",
      "valueType": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "targetEntity": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    }
  ],
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 
  // ... (truncated for brevity)
```

---

### `DELETE` /api/composite-type/{id}

**Delete Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `DELETE` /api/composite-type/async/{id}

**Delete an object asynchronously (returns a Job ID)**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example** (Asynchronous Job)

```json
{
  "id": 0,
  "status": "COMPLETED",
  "startTime": "2026-02-26T04:37:56.320Z",
  "endTime": "2026-02-26T04:37:56.320Z"
}
```

---

## Custom Property

Manage Custom Property objects — user-defined properties that extend standard objects.

### `PUT` /api/custom-property

**Update Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "forObjectType": "BUSINESS_TERM",
  "propertyType": "Text",
  "targetObjectType": "Attribute",
  "options": [
    {
      "id": 0,
      "value": "string"
    }
  ],
  "orderOptionsAlphabetically": true,
  "multiselection": true,
  "mandatory": true,
  "defaultValue": {
    "value": "string",
    "reference": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "processReference": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "dataSetReference": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSetType": "Logical",
      "dataSetDomains": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "dataSource": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string",
        "dataSourceType": "ACCURITY_EDGE_PULL"
      }
    },
    "dataStructureReference": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "entityReference": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "attri
  // ... (truncated for brevity)
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "forObjectType": "BUSINESS_TERM",
  "propertyType": "Text",
  "targetObjectType": "Attribute",
  "options": [
    {
      "id": 0,
      "value": "string"
    }
  ],
  "orderOptionsAlphabetically": true,
  "multiselection": true,
  "mandatory": true,
  "defaultValue": {
    "value": "string",
    "reference": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "processReference": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "dataSetReference": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSetType": "Logical",
      "dataSetDomains": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "dataSource": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string",
        "dataSourceType": "ACCURITY_EDGE_PULL"
      }
    },
    "dataStructureReference": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "entityReference": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "attri
  // ... (truncated for brevity)
```

---

### `POST` /api/custom-property

**Create Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "forObjectType": "BUSINESS_TERM",
  "propertyType": "Text",
  "targetObjectType": "Attribute",
  "options": [
    {
      "id": 0,
      "value": "string"
    }
  ],
  "orderOptionsAlphabetically": true,
  "multiselection": true,
  "mandatory": true,
  "defaultValue": {
    "value": "string",
    "reference": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "processReference": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "dataSetReference": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSetType": "Logical",
      "dataSetDomains": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "dataSource": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string",
        "dataSourceType": "ACCURITY_EDGE_PULL"
      }
    },
    "dataStructureReference": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "entityReference": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "attri
  // ... (truncated for brevity)
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "forObjectType": "BUSINESS_TERM",
  "propertyType": "Text",
  "targetObjectType": "Attribute",
  "options": [
    {
      "id": 0,
      "value": "string"
    }
  ],
  "orderOptionsAlphabetically": true,
  "multiselection": true,
  "mandatory": true,
  "defaultValue": {
    "value": "string",
    "reference": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "processReference": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "dataSetReference": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSetType": "Logical",
      "dataSetDomains": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "dataSource": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string",
        "dataSourceType": "ACCURITY_EDGE_PULL"
      }
    },
    "dataStructureReference": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "entityReference": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "attri
  // ... (truncated for brevity)
```

---

### `POST` /api/custom-property/search

**Search Objects**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "startFrom": 0,
  "maxResults": 0,
  "filters": [
    {
      "type": "SIMPLE_QUERY",
      "property": "string",
      "value": "string",
      "timezone": "string",
      "relationType": "RELATED_TO"
    }
  ],
  "sort": {
    "type": "ASCENDING",
    "property": "string"
  },
  "asOfTime": 0
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "size": 0,
  "rows": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
      "changedBy": {
        "id": 0,
        "name": "string"
      },
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "chips": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "forObjectType": "BUSINESS_TERM",
      "propertyType": "Text",
      "targetObjectType": "Attribute",
      "options": [
        {
          "id": 0,
          "value": "string"
        }
      ],
      "orderOptionsAlphabetically": true,
      "multiselection": true,
      "mandatory": true,
      "defaultValue": {
        "value": "string",
        "reference": {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        },
        "processReference": {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        },
        "dataSetReference": {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string",
          "dataSetType": "Logical",
          "dataSetDomains": [
            {
              "id": 0,
              "name": "string",
              "description": {
                "plainTextValue": "string",
                "formattedValue": "string"
              },
              "objectType": "string"
            }
          ],
          "dataSource": {
            "id": 0,
            "name": "string",
            "description": {
              "plainTextValue": "string",
              "formattedValue": "string"
            },
            "objectType": "string",
            "dataSourceType": "ACCURITY_EDGE_PULL"
          }
        },
        "dataStructureReference": {
  
  // ... (truncated for brevity)
```

---

### `GET` /api/custom-property/{id}

**Find Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "forObjectType": "BUSINESS_TERM",
  "propertyType": "Text",
  "targetObjectType": "Attribute",
  "options": [
    {
      "id": 0,
      "value": "string"
    }
  ],
  "orderOptionsAlphabetically": true,
  "multiselection": true,
  "mandatory": true,
  "defaultValue": {
    "value": "string",
    "reference": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "processReference": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "dataSetReference": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSetType": "Logical",
      "dataSetDomains": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "dataSource": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string",
        "dataSourceType": "ACCURITY_EDGE_PULL"
      }
    },
    "dataStructureReference": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "entityReference": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    },
    "attri
  // ... (truncated for brevity)
```

---

### `DELETE` /api/custom-property/{id}

**Delete Object**

**Parameters**

No parameters.
**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `DELETE` /api/custom-property/async/{id}

**Delete an object asynchronously (returns a Job ID)**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example** (Asynchronous Job)

```json
{
  "id": 0,
  "status": "COMPLETED",
  "startTime": "2026-02-26T04:37:56.374Z",
  "endTime": "2026-02-26T04:37:56.374Z"
}
```

---

## Custom Property Group

Manage Custom Property Group objects — logical groupings of custom properties.

### `PUT` /api/custom-property-group

**Update Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "collapsedByDefault": true,
  "groupOrder": 0,
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "collapsedByDefault": true,
  "groupOrder": 0,
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

---

### `POST` /api/custom-property-group

**Create Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "collapsedByDefault": true,
  "groupOrder": 0,
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "collapsedByDefault": true,
  "groupOrder": 0,
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

---

### `POST` /api/custom-property-group/search

**Search Objects**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "startFrom": 0,
  "maxResults": 0,
  "filters": [
    {
      "type": "SIMPLE_QUERY",
      "property": "string",
      "value": "string",
      "timezone": "string",
      "relationType": "RELATED_TO"
    }
  ],
  "sort": {
    "type": "ASCENDING",
    "property": "string"
  },
  "asOfTime": 0
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "size": 0,
  "rows": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
      "changedBy": {
        "id": 0,
        "name": "string"
      },
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "chips": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "collapsedByDefault": true,
      "groupOrder": 0,
      "childrenCounts": {
        "id": 0,
        "type": "string",
        "domainsCount": 0,
        "domainOwnersCount": 0,
        "dataStewardsCount": 0,
        "dataAssetsCount": 0,
        "dataSetsCount": 0,
        "dataStructuresCount": 0,
        "dataFieldsCount": 0,
        "businessTermsCount": 0,
        "entitiesCount": 0,
        "referenceAttributeTargetEntitiesCount": 0,
        "attributesCount": 0,
        "calculationRulesCount": 0,
        "attributeDefinitionsCount": 0,
        "compositeTypesCount": 0,
        "customPropertiesCount": 0,
        "businessRulesCount": 0,
        "businessModelMappingsCount": 0,
        "processesCount": 0,
        "processStepsCount": 0,
        "processMappingsCount": 0,
        "technicalDataMappingsCount": 0,
        "commentsCount": 0,
        "objectType": "string"
      },
      "activeNotifications": {
        "COMMENT_UPDATE": true,
        "OBJECT_UPDATE": true
      }
    }
  ],
  "existingObjects": 0,
  "maximumObjects": 0,
  "additionalExistingObjects": 0,
  "additionalMaximumObjects": 0
}
```

---

### `GET` /api/custom-property-group/{id}

**Find Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "collapsedByDefault": true,
  "groupOrder": 0,
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

---

### `DELETE` /api/custom-property-group/{id}

**Delete Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `DELETE` /api/custom-property-group/async/{id}

**Delete an object asynchronously (returns a Job ID)**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example** (Asynchronous Job)

```json
{
  "id": 0,
  "status": "COMPLETED",
  "startTime": "2026-02-26T04:37:56.429Z",
  "endTime": "2026-02-26T04:37:56.429Z"
}
```

---

## Data Asset

Manage Data Asset objects — representations of data assets in the organization.

### `PUT` /api/data-asset

**Update Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "parent": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "dataSets": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSetType": "Logical",
      "dataSetDomains": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "dataSource": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string",
        "dataSourceType": "ACCURITY_EDGE_PULL"
      }
    }
  ],
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0
  // ... (truncated for brevity)
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "parent": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "dataSets": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSetType": "Logical",
      "dataSetDomains": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "dataSource": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string",
        "dataSourceType": "ACCURITY_EDGE_PULL"
      }
    }
  ],
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0
  // ... (truncated for brevity)
```

---

### `POST` /api/data-asset

**Create Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "parent": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "dataSets": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSetType": "Logical",
      "dataSetDomains": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "dataSource": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string",
        "dataSourceType": "ACCURITY_EDGE_PULL"
      }
    }
  ],
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0
  // ... (truncated for brevity)
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "parent": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "dataSets": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSetType": "Logical",
      "dataSetDomains": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "dataSource": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string",
        "dataSourceType": "ACCURITY_EDGE_PULL"
      }
    }
  ],
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0
  // ... (truncated for brevity)
```

---

### `POST` /api/data-asset/search

**Search Objects**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "startFrom": 0,
  "maxResults": 0,
  "filters": [
    {
      "type": "SIMPLE_QUERY",
      "property": "string",
      "value": "string",
      "timezone": "string",
      "relationType": "RELATED_TO"
    }
  ],
  "sort": {
    "type": "ASCENDING",
    "property": "string"
  },
  "asOfTime": 0
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "size": 0,
  "rows": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
      "changedBy": {
        "id": 0,
        "name": "string"
      },
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "chips": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "tags": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "status": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "parent": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "dataSets": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string",
          "dataSetType": "Logical",
          "dataSetDomains": [
            {
              "id": 0,
              "name": "string",
              "description": {
                "plainTextValue": "string",
                "formattedValue": "string"
              },
              "objectType": "string"
            }
          ],
          "dataSource": {
            "id": 0,
            "name": "string",
            "description": {
              "plainTextValue": "string",
              "formattedValue": "string"
            },
            "objectType": "string",
            "dataSourceType": "ACCURITY_EDGE_PULL"
          }
        }
      ],
      "customPropertyValues": {
        "1": [
          "string"
        ],
        "2": [
          "string"
        ]
      },
      "childrenCounts": {
        "id": 0,
      
  // ... (truncated for brevity)
```

---

### `GET` /api/data-asset/{id}

**Find Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "parent": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "dataSets": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSetType": "Logical",
      "dataSetDomains": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "dataSource": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string",
        "dataSourceType": "ACCURITY_EDGE_PULL"
      }
    }
  ],
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0
  // ... (truncated for brevity)
```

---

### `DELETE` /api/data-asset/{id}

**Delete Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `DELETE` /api/data-asset/async/{id}

**Delete an object asynchronously (returns a Job ID)**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example** (Asynchronous Job)

```json
{
  "id": 0,
  "status": "COMPLETED",
  "startTime": "2026-02-26T04:37:56.490Z",
  "endTime": "2026-02-26T04:37:56.490Z"
}
```

---

## Data Field

Manage Data Field objects — individual fields within data structures or data sets.

### `PUT` /api/data-field

**Update Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "dataSet": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string",
    "dataSetType": "Logical",
    "dataSetDomains": [
      {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    ],
    "dataSource": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSourceType": "ACCURITY_EDGE_PULL"
    }
  },
  "dataStructure": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string",
    "dataSet": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSetType": "Logical",
      "dataSetDomains": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "dataSource": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "s
  // ... (truncated for brevity)
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "dataSet": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string",
    "dataSetType": "Logical",
    "dataSetDomains": [
      {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    ],
    "dataSource": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSourceType": "ACCURITY_EDGE_PULL"
    }
  },
  "dataStructure": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string",
    "dataSet": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSetType": "Logical",
      "dataSetDomains": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "dataSource": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "s
  // ... (truncated for brevity)
```

---

### `POST` /api/data-field

**Create Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "dataSet": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string",
    "dataSetType": "Logical",
    "dataSetDomains": [
      {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    ],
    "dataSource": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSourceType": "ACCURITY_EDGE_PULL"
    }
  },
  "dataStructure": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string",
    "dataSet": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSetType": "Logical",
      "dataSetDomains": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "dataSource": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "s
  // ... (truncated for brevity)
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "dataSet": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string",
    "dataSetType": "Logical",
    "dataSetDomains": [
      {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    ],
    "dataSource": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSourceType": "ACCURITY_EDGE_PULL"
    }
  },
  "dataStructure": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string",
    "dataSet": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSetType": "Logical",
      "dataSetDomains": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "dataSource": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "s
  // ... (truncated for brevity)
```

---

### `POST` /api/data-field/{id}/profile

**Profile Data Field**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `POST` /api/data-field/search

**Search Objects**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "startFrom": 0,
  "maxResults": 0,
  "filters": [
    {
      "type": "SIMPLE_QUERY",
      "property": "string",
      "value": "string",
      "timezone": "string",
      "relationType": "RELATED_TO"
    }
  ],
  "sort": {
    "type": "ASCENDING",
    "property": "string"
  },
  "asOfTime": 0
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "size": 0,
  "rows": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
      "changedBy": {
        "id": 0,
        "name": "string"
      },
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "chips": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "tags": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "status": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "dataSet": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string",
        "dataSetType": "Logical",
        "dataSetDomains": [
          {
            "id": 0,
            "name": "string",
            "description": {
              "plainTextValue": "string",
              "formattedValue": "string"
            },
            "objectType": "string"
          }
        ],
        "dataSource": {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string",
          "dataSourceType": "ACCURITY_EDGE_PULL"
        }
      },
      "dataStructure": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string",
        "dataSet": {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string",
          "dataSetType": "Logical",
      
  // ... (truncated for brevity)
```

---

### `GET` /api/data-field/{id}

**Find Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "dataSet": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string",
    "dataSetType": "Logical",
    "dataSetDomains": [
      {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    ],
    "dataSource": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSourceType": "ACCURITY_EDGE_PULL"
    }
  },
  "dataStructure": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string",
    "dataSet": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSetType": "Logical",
      "dataSetDomains": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "dataSource": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "s
  // ... (truncated for brevity)
```

---

### `DELETE` /api/data-field/{id}

**Delete Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `DELETE` /api/data-field/async/{id}

**Delete an object asynchronously (returns a Job ID)**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example** (Asynchronous Job)

```json
{
  "id": 0,
  "status": "COMPLETED",
  "startTime": "2026-02-26T04:37:56.566Z",
  "endTime": "2026-02-26T04:37:56.566Z"
}
```

---

## Data Set

Manage Data Set objects — collections of data records from a data source.

### `PUT` /api/data-set

**Update Object**

**Parameters**

No parameters.
**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `POST` /api/data-set

**Create Object**

**Parameters**

No parameters.
**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `POST` /api/data-set/search

**Search Objects**

**Parameters**

No parameters.
**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `GET` /api/data-set/{id}

**Find Object**

**Parameters**

No parameters.
**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `DELETE` /api/data-set/{id}

**Delete Object**

**Parameters**

No parameters.
**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `GET` /api/data-set/sync/{dataSetId}/{scanUuid}

**Synchronize Data Set**

**Parameters**

No parameters.
**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `DELETE` /api/data-set/async/{id}

**Delete an object asynchronously (returns a Job ID)**

**Parameters**

No parameters.
**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

## Data Source

Manage Data Source objects — connections to external data systems.

### `PUT` /api/data-source

**Update Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "dataSourceType": "ACCURITY_EDGE_PULL",
  "host": "string",
  "port": 0,
  "database": "string",
  "schema": "string",
  "authenticationDatabase": "string",
  "oracleConnectionType": "SID",
  "useJdbcUrl": true,
  "jdbcUrl": "string",
  "dataSourceUsername": "string",
  "dataSourcePassword": "string",
  "fileName": "string",
  "edgeComponentUrl": "string",
  "edgeDataSourceReference": {
    "edgeDataSourceId": "string",
    "edgeDataSourceName": "string"
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "dataSourceType": "ACCURITY_EDGE_PULL",
  "host": "string",
  "port": 0,
  "database": "string",
  "schema": "string",
  "authenticationDatabase": "string",
  "oracleConnectionType": "SID",
  "useJdbcUrl": true,
  "jdbcUrl": "string",
  "dataSourceUsername": "string",
  "dataSourcePassword": "string",
  "fileName": "string",
  "edgeComponentUrl": "string",
  "edgeDataSourceReference": {
    "edgeDataSourceId": "string",
    "edgeDataSourceName": "string"
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

---

### `POST` /api/data-source

**Create Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "dataSourceType": "ACCURITY_EDGE_PULL",
  "host": "string",
  "port": 0,
  "database": "string",
  "schema": "string",
  "authenticationDatabase": "string",
  "oracleConnectionType": "SID",
  "useJdbcUrl": true,
  "jdbcUrl": "string",
  "dataSourceUsername": "string",
  "dataSourcePassword": "string",
  "fileName": "string",
  "edgeComponentUrl": "string",
  "edgeDataSourceReference": {
    "edgeDataSourceId": "string",
    "edgeDataSourceName": "string"
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "dataSourceType": "ACCURITY_EDGE_PULL",
  "host": "string",
  "port": 0,
  "database": "string",
  "schema": "string",
  "authenticationDatabase": "string",
  "oracleConnectionType": "SID",
  "useJdbcUrl": true,
  "jdbcUrl": "string",
  "dataSourceUsername": "string",
  "dataSourcePassword": "string",
  "fileName": "string",
  "edgeComponentUrl": "string",
  "edgeDataSourceReference": {
    "edgeDataSourceId": "string",
    "edgeDataSourceName": "string"
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

---

### `POST` /api/data-source/search

**Search Objects**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "startFrom": 0,
  "maxResults": 0,
  "filters": [
    {
      "type": "SIMPLE_QUERY",
      "property": "string",
      "value": "string",
      "timezone": "string",
      "relationType": "RELATED_TO"
    }
  ],
  "sort": {
    "type": "ASCENDING",
    "property": "string"
  },
  "asOfTime": 0
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "size": 0,
  "rows": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
      "changedBy": {
        "id": 0,
        "name": "string"
      },
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "chips": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "dataSourceType": "ACCURITY_EDGE_PULL",
      "host": "string",
      "port": 0,
      "database": "string",
      "schema": "string",
      "authenticationDatabase": "string",
      "oracleConnectionType": "SID",
      "useJdbcUrl": true,
      "jdbcUrl": "string",
      "dataSourceUsername": "string",
      "dataSourcePassword": "string",
      "fileName": "string",
      "edgeComponentUrl": "string",
      "edgeDataSourceReference": {
        "edgeDataSourceId": "string",
        "edgeDataSourceName": "string"
      },
      "childrenCounts": {
        "id": 0,
        "type": "string",
        "domainsCount": 0,
        "domainOwnersCount": 0,
        "dataStewardsCount": 0,
        "dataAssetsCount": 0,
        "dataSetsCount": 0,
        "dataStructuresCount": 0,
        "dataFieldsCount": 0,
        "businessTermsCount": 0,
        "entitiesCount": 0,
        "referenceAttributeTargetEntitiesCount": 0,
        "attributesCount": 0,
        "calculationRulesCount": 0,
        "attributeDefinitionsCount": 0,
        "compositeTypesCount": 0,
        "customPropertiesCount": 0,
        "businessRulesCount": 0,
        "businessModelMappingsCount": 0,
        "processesCount": 0,
        "processStepsCount": 0,
        "processMappingsCount": 0,
        "technicalDataMappingsCount": 0,
        "commentsCount": 0,
        "objectType": "string"
      },
      "activeNotifications": {
        "COMMENT_UPDATE": true,
        "OBJECT_UPDATE": true
      }
    }
  ],
  "existingObjects": 0,
  "maximumObjects": 0,
  "additionalExistingObjects": 0,
  "additionalMaximumObjects": 0
}
```

---

### `GET` /api/data-source/{id}

**Find Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "dataSourceType": "ACCURITY_EDGE_PULL",
  "host": "string",
  "port": 0,
  "database": "string",
  "schema": "string",
  "authenticationDatabase": "string",
  "oracleConnectionType": "SID",
  "useJdbcUrl": true,
  "jdbcUrl": "string",
  "dataSourceUsername": "string",
  "dataSourcePassword": "string",
  "fileName": "string",
  "edgeComponentUrl": "string",
  "edgeDataSourceReference": {
    "edgeDataSourceId": "string",
    "edgeDataSourceName": "string"
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

---

### `DELETE` /api/data-source/{id}

**Delete Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `DELETE` /api/data-source/async/{id}

**Delete an object asynchronously (returns a Job ID)**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example** (Asynchronous Job)

```json
{
  "id": 0,
  "status": "COMPLETED",
  "startTime": "2026-02-26T04:37:56.617Z",
  "endTime": "2026-02-26T04:37:56.617Z"
}
```

---

## Data Structure

Manage Data Structure objects — schemas or table definitions within a data source.

### `PUT` /api/data-structure

**Update Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "comments": "string",
  "dataSource": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "dataSet": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string",
    "dataSetType": "Logical",
    "dataSetDomains": [
      {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    ],
    "dataSource": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSourceType": "ACCURITY_EDGE_PULL"
    }
  },
  "dataStructureType": "LOGICAL",
  "primaryKeys": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataStructure": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string",
        "dataSet": {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "
  // ... (truncated for brevity)
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "comments": "string",
  "dataSource": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "dataSet": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string",
    "dataSetType": "Logical",
    "dataSetDomains": [
      {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    ],
    "dataSource": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSourceType": "ACCURITY_EDGE_PULL"
    }
  },
  "dataStructureType": "LOGICAL",
  "primaryKeys": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataStructure": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string",
        "dataSet": {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "
  // ... (truncated for brevity)
```

---

### `POST` /api/data-structure

**Create Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "comments": "string",
  "dataSource": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "dataSet": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string",
    "dataSetType": "Logical",
    "dataSetDomains": [
      {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    ],
    "dataSource": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSourceType": "ACCURITY_EDGE_PULL"
    }
  },
  "dataStructureType": "LOGICAL",
  "primaryKeys": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataStructure": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string",
        "dataSet": {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "
  // ... (truncated for brevity)
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "comments": "string",
  "dataSource": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "dataSet": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string",
    "dataSetType": "Logical",
    "dataSetDomains": [
      {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    ],
    "dataSource": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSourceType": "ACCURITY_EDGE_PULL"
    }
  },
  "dataStructureType": "LOGICAL",
  "primaryKeys": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataStructure": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string",
        "dataSet": {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "
  // ... (truncated for brevity)
```

---

### `POST` /api/data-structure/search

**Search Objects**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "startFrom": 0,
  "maxResults": 0,
  "filters": [
    {
      "type": "SIMPLE_QUERY",
      "property": "string",
      "value": "string",
      "timezone": "string",
      "relationType": "RELATED_TO"
    }
  ],
  "sort": {
    "type": "ASCENDING",
    "property": "string"
  },
  "asOfTime": 0
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "size": 0,
  "rows": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
      "changedBy": {
        "id": 0,
        "name": "string"
      },
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "chips": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "tags": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "comments": "string",
      "dataSource": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "status": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "dataSet": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string",
        "dataSetType": "Logical",
        "dataSetDomains": [
          {
            "id": 0,
            "name": "string",
            "description": {
              "plainTextValue": "string",
              "formattedValue": "string"
            },
            "objectType": "string"
          }
        ],
        "dataSource": {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string",
          "dataSourceType": "ACCURITY_EDGE_PULL"
        }
      },
      "dataStructureType": "LOGICAL",
      "primaryKeys": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
     
  // ... (truncated for brevity)
```

---

### `GET` /api/data-structure/{id}

**Find Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "comments": "string",
  "dataSource": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "dataSet": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string",
    "dataSetType": "Logical",
    "dataSetDomains": [
      {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    ],
    "dataSource": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSourceType": "ACCURITY_EDGE_PULL"
    }
  },
  "dataStructureType": "LOGICAL",
  "primaryKeys": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataStructure": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string",
        "dataSet": {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "
  // ... (truncated for brevity)
```

---

### `DELETE` /api/data-structure/{id}

**Delete Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `DELETE` /api/data-structure/async/{id}

**Delete an object asynchronously (returns a Job ID)**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example** (Asynchronous Job)

```json
{
  "id": 0,
  "status": "COMPLETED",
  "startTime": "2026-02-26T04:37:56.702Z",
  "endTime": "2026-02-26T04:37:56.702Z"
}
```

---

## Domain

Manage Domain objects — organizational units that group business terms and entities.

### `PUT` /api/domain

**Update Object**

**Parameters**

No parameters.
**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `POST` /api/domain

**Create Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  },
  "domainOwners": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "dataStewards": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ]
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  },
  "domainOwners": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "dataStewards": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ]
}
```

---

### `POST` /api/domain/search

**Search Objects**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "startFrom": 0,
  "maxResults": 0,
  "filters": [
    {
      "type": "SIMPLE_QUERY",
      "property": "string",
      "value": "string",
      "timezone": "string",
      "relationType": "RELATED_TO"
    }
  ],
  "sort": {
    "type": "ASCENDING",
    "property": "string"
  },
  "asOfTime": 0
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "size": 0,
  "rows": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
      "changedBy": {
        "id": 0,
        "name": "string"
      },
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "chips": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "customPropertyValues": {
        "1": [
          "string"
        ],
        "2": [
          "string"
        ]
      },
      "childrenCounts": {
        "id": 0,
        "type": "string",
        "domainsCount": 0,
        "domainOwnersCount": 0,
        "dataStewardsCount": 0,
        "dataAssetsCount": 0,
        "dataSetsCount": 0,
        "dataStructuresCount": 0,
        "dataFieldsCount": 0,
        "businessTermsCount": 0,
        "entitiesCount": 0,
        "referenceAttributeTargetEntitiesCount": 0,
        "attributesCount": 0,
        "calculationRulesCount": 0,
        "attributeDefinitionsCount": 0,
        "compositeTypesCount": 0,
        "customPropertiesCount": 0,
        "businessRulesCount": 0,
        "businessModelMappingsCount": 0,
        "processesCount": 0,
        "processStepsCount": 0,
        "processMappingsCount": 0,
        "technicalDataMappingsCount": 0,
        "commentsCount": 0,
        "objectType": "string"
      },
      "activeNotifications": {
        "COMMENT_UPDATE": true,
        "OBJECT_UPDATE": true
      },
      "domainOwners": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "dataStewards": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ]
    }
  ],
  "existingObjects": 0,
  "maximumObjects": 0,
  "additionalExistingObjects": 0,
  "additionalMaximumObjects": 0
}
```

---

### `GET` /api/domain/{id}

**Find Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  },
  "domainOwners": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "dataStewards": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ]
}
```

---

### `DELETE` /api/domain/{id}

**Delete Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `DELETE` /api/domain/async/{id}

**Delete an object asynchronously (returns a Job ID)**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example** (Asynchronous Job)

```json
{
  "id": 0,
  "status": "COMPLETED",
  "startTime": "2026-02-26T04:37:56.748Z",
  "endTime": "2026-02-26T04:37:56.748Z"
}
```

---

## Entity

Manage Entity objects — business entities (e.g., Customer, Product) in the glossary.

### `PUT` /api/entity

**Update Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "basedOnBusinessTerm": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "entityType": "Main",
  "parent": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  },
  "keepInheritedAttributes": true
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "basedOnBusinessTerm": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "entityType": "Main",
  "parent": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  },
  "keepInheritedAttributes": true
}
```

---

### `POST` /api/entity

**Create Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "basedOnBusinessTerm": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "entityType": "Main",
  "parent": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  },
  "keepInheritedAttributes": true
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "basedOnBusinessTerm": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "entityType": "Main",
  "parent": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  },
  "keepInheritedAttributes": true
}
```

---

### `POST` /api/entity/search

**Search Objects**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "startFrom": 0,
  "maxResults": 0,
  "filters": [
    {
      "type": "SIMPLE_QUERY",
      "property": "string",
      "value": "string",
      "timezone": "string",
      "relationType": "RELATED_TO"
    }
  ],
  "sort": {
    "type": "ASCENDING",
    "property": "string"
  },
  "asOfTime": 0
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "size": 0,
  "rows": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
      "changedBy": {
        "id": 0,
        "name": "string"
      },
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "chips": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "tags": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "basedOnBusinessTerm": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "status": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "entityType": "Main",
      "parent": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "customPropertyValues": {
        "1": [
          "string"
        ],
        "2": [
          "string"
        ]
      },
      "childrenCounts": {
        "id": 0,
        "type": "string",
        "domainsCount": 0,
        "domainOwnersCount": 0,
        "dataStewardsCount": 0,
        "dataAssetsCount": 0,
        "dataSetsCount": 0,
        "dataStructuresCount": 0,
        "dataFieldsCount": 0,
        "businessTermsCount": 0,
        "entitiesCount": 0,
        "referenceAttributeTargetEntitiesCount": 0,
        "attributesCount": 0,
        "calculationRulesCount": 0,
        "attributeDefinitionsCount": 0,
        "compositeTypesCount": 0,
        "customPropertiesCount": 0,
        "businessRulesCount": 0,
        "businessModelMappingsCount": 0,
        "processesCount": 0,
        "pro
  // ... (truncated for brevity)
```

---

### `GET` /api/entity/{id}

**Find Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "basedOnBusinessTerm": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "entityType": "Main",
  "parent": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  },
  "keepInheritedAttributes": true
}
```

---

### `DELETE` /api/entity/{id}

**Delete Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `DELETE` /api/entity/async/{id}

**Delete an object asynchronously (returns a Job ID)**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example** (Asynchronous Job)

```json
{
  "id": 0,
  "status": "COMPLETED",
  "startTime": "2026-02-26T04:37:56.807Z",
  "endTime": "2026-02-26T04:37:56.807Z"
}
```

---

## Process

Manage Process objects — business processes in the organization.

### `PUT` /api/process

**Update Object**

**Parameters**

No parameters.
**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `POST` /api/process

**Create Object**

**Parameters**

No parameters.
**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `POST` /api/process/search

**Search Objects**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "startFrom": 0,
  "maxResults": 0,
  "filters": [
    {
      "type": "SIMPLE_QUERY",
      "property": "string",
      "value": "string",
      "timezone": "string",
      "relationType": "RELATED_TO"
    }
  ],
  "sort": {
    "type": "ASCENDING",
    "property": "string"
  },
  "asOfTime": 0
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "size": 0,
  "rows": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
      "changedBy": {
        "id": 0,
        "name": "string"
      },
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "chips": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "tags": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "status": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "customPropertyValues": {
        "1": [
          "string"
        ],
        "2": [
          "string"
        ]
      },
      "childrenCounts": {
        "id": 0,
        "type": "string",
        "domainsCount": 0,
        "domainOwnersCount": 0,
        "dataStewardsCount": 0,
        "dataAssetsCount": 0,
        "dataSetsCount": 0,
        "dataStructuresCount": 0,
        "dataFieldsCount": 0,
        "businessTermsCount": 0,
        "entitiesCount": 0,
        "referenceAttributeTargetEntitiesCount": 0,
        "attributesCount": 0,
        "calculationRulesCount": 0,
        "attributeDefinitionsCount": 0,
        "compositeTypesCount": 0,
        "customPropertiesCount": 0,
        "businessRulesCount": 0,
        "businessModelMappingsCount": 0,
        "processesCount": 0,
        "processStepsCount": 0,
        "processMappingsCount": 0,
        "technicalDataMappingsCount": 0,
        "commentsCount": 0,
        "objectType": "string"
      },
      "activeNotifications": {
        "COMMENT_UPDATE": true,
        "OBJECT_UPDATE": true
      }
    }
  ],
  "existingObjects": 0,
  "maximumObjects": 0,
  "additionalExistingObjects": 0,
  "additionalMaximumObjects": 0
}
```

---

### `GET` /api/process/{id}

**Find Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

---

### `DELETE` /api/process/{id}

**Delete Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `DELETE` /api/process/async/{id}

**Delete an object asynchronously (returns a Job ID)**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example** (Asynchronous Job)

```json
{
  "id": 0,
  "status": "COMPLETED",
  "startTime": "2026-02-26T04:37:56.840Z",
  "endTime": "2026-02-26T04:37:56.840Z"
}
```

---

## Process Mapping

Manage Process Mapping objects — mappings between processes and other objects.

### `PUT` /api/process-mapping

**Update Object**

**Parameters**

No parameters.
**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `POST` /api/process-mapping

**Create Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "processMappingType": "Input",
  "processMappingBasedOnType": "Process",
  "process": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "processStep": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "processMappingTargetEntities": [
    {
      "id": 0,
      "entity": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "objectType": "string"
    }
  ],
  "processMappingTargetAttributes": [
    {
      "id": 0,
      "entity": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "attributeDefinition": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "attribute": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "objectType": "string"
    }
  ],
  // ... (truncated for brevity)
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "processMappingType": "Input",
  "processMappingBasedOnType": "Process",
  "process": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "processStep": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "processMappingTargetEntities": [
    {
      "id": 0,
      "entity": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "objectType": "string"
    }
  ],
  "processMappingTargetAttributes": [
    {
      "id": 0,
      "entity": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "attributeDefinition": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "attribute": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "objectType": "string"
    }
  ],
  // ... (truncated for brevity)
```

---

### `POST` /api/process-mapping/search

**Search Objects**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "startFrom": 0,
  "maxResults": 0,
  "filters": [
    {
      "type": "SIMPLE_QUERY",
      "property": "string",
      "value": "string",
      "timezone": "string",
      "relationType": "RELATED_TO"
    }
  ],
  "sort": {
    "type": "ASCENDING",
    "property": "string"
  },
  "asOfTime": 0
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "size": 0,
  "rows": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
      "changedBy": {
        "id": 0,
        "name": "string"
      },
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "chips": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "tags": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "status": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "processMappingType": "Input",
      "processMappingBasedOnType": "Process",
      "process": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "processStep": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "processMappingTargetEntities": [
        {
          "id": 0,
          "entity": {
            "id": 0,
            "name": "string",
            "description": {
              "plainTextValue": "string",
              "formattedValue": "string"
            },
            "objectType": "string"
          },
          "objectType": "string"
        }
      ],
      "processMappingTargetAttributes": [
        {
          "id": 0,
          "entity": {
            "id": 0,
            "name": "string",
            "description": {
              "plainTextValue": "string",
              "formattedValue": "string"
            },
            "objectType": "string"
          },
          "attributeDefinition": {
            "id": 0,
            "name": "st
  // ... (truncated for brevity)
```

---

### `GET` /api/process-mapping/{id}

**Find Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "processMappingType": "Input",
  "processMappingBasedOnType": "Process",
  "process": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "processStep": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "processMappingTargetEntities": [
    {
      "id": 0,
      "entity": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "objectType": "string"
    }
  ],
  "processMappingTargetAttributes": [
    {
      "id": 0,
      "entity": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "attributeDefinition": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "attribute": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "objectType": "string"
    }
  ],
  // ... (truncated for brevity)
```

---

### `DELETE` /api/process-mapping/{id}

**Delete Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `DELETE` /api/process-mapping/async/{id}

**Delete an object asynchronously (returns a Job ID)**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example** (Asynchronous Job)

```json
{
  "id": 0,
  "status": "COMPLETED",
  "startTime": "2026-02-26T04:37:56.892Z",
  "endTime": "2026-02-26T04:37:56.892Z"
}
```

---

## Process Step

Manage Process Step objects — individual steps within a business process.

### `PUT` /api/process-step

**Update Object**

**Parameters**

No parameters.
**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `POST` /api/process-step

**Create Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "process": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "process": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

---

### `POST` /api/process-step/search

**Search Objects**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "startFrom": 0,
  "maxResults": 0,
  "filters": [
    {
      "type": "SIMPLE_QUERY",
      "property": "string",
      "value": "string",
      "timezone": "string",
      "relationType": "RELATED_TO"
    }
  ],
  "sort": {
    "type": "ASCENDING",
    "property": "string"
  },
  "asOfTime": 0
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "size": 0,
  "rows": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
      "changedBy": {
        "id": 0,
        "name": "string"
      },
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "chips": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "tags": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "status": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "process": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "customPropertyValues": {
        "1": [
          "string"
        ],
        "2": [
          "string"
        ]
      },
      "childrenCounts": {
        "id": 0,
        "type": "string",
        "domainsCount": 0,
        "domainOwnersCount": 0,
        "dataStewardsCount": 0,
        "dataAssetsCount": 0,
        "dataSetsCount": 0,
        "dataStructuresCount": 0,
        "dataFieldsCount": 0,
        "businessTermsCount": 0,
        "entitiesCount": 0,
        "referenceAttributeTargetEntitiesCount": 0,
        "attributesCount": 0,
        "calculationRulesCount": 0,
        "attributeDefinitionsCount": 0,
        "compositeTypesCount": 0,
        "customPropertiesCount": 0,
        "businessRulesCount": 0,
        "businessModelMappingsCount": 0,
        "processesCount": 0,
        "processStepsCount": 0,
        "processMappingsCount": 0,
        "technicalDataMappingsCount": 0,
        "commentsCount": 0,
        "objectType": "string"
      },
      "activeNotifications": {
        "COMMENT_UPDATE": true,
        "OBJECT_UPDATE": tr
  // ... (truncated for brevity)
```

---

### `GET` /api/process-step/{id}

**Find Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "process": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

---

### `DELETE` /api/process-step/{id}

**Delete Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `DELETE` /api/process-step/async/{id}

**Delete an object asynchronously (returns a Job ID)**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example** (Asynchronous Job)

```json
{
  "id": 0,
  "status": "COMPLETED",
  "startTime": "2026-02-26T04:37:56.937Z",
  "endTime": "2026-02-26T04:37:56.937Z"
}
```

---

## Requirement

Manage Requirement objects — business or technical requirements.

### `PUT` /api/requirement

**Update Object**

**Parameters**

No parameters.
**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `POST` /api/requirement

**Create Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

---

### `POST` /api/requirement/search

**Search Objects**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "startFrom": 0,
  "maxResults": 0,
  "filters": [
    {
      "type": "SIMPLE_QUERY",
      "property": "string",
      "value": "string",
      "timezone": "string",
      "relationType": "RELATED_TO"
    }
  ],
  "sort": {
    "type": "ASCENDING",
    "property": "string"
  },
  "asOfTime": 0
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "size": 0,
  "rows": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
      "changedBy": {
        "id": 0,
        "name": "string"
      },
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "chips": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "tags": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "status": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "customPropertyValues": {
        "1": [
          "string"
        ],
        "2": [
          "string"
        ]
      },
      "childrenCounts": {
        "id": 0,
        "type": "string",
        "domainsCount": 0,
        "domainOwnersCount": 0,
        "dataStewardsCount": 0,
        "dataAssetsCount": 0,
        "dataSetsCount": 0,
        "dataStructuresCount": 0,
        "dataFieldsCount": 0,
        "businessTermsCount": 0,
        "entitiesCount": 0,
        "referenceAttributeTargetEntitiesCount": 0,
        "attributesCount": 0,
        "calculationRulesCount": 0,
        "attributeDefinitionsCount": 0,
        "compositeTypesCount": 0,
        "customPropertiesCount": 0,
        "businessRulesCount": 0,
        "businessModelMappingsCount": 0,
        "processesCount": 0,
        "processStepsCount": 0,
        "processMappingsCount": 0,
        "technicalDataMappingsCount": 0,
        "commentsCount": 0,
        "objectType": "string"
      },
      "activeNotifications": {
        "COMMENT_UPDATE": true,
        "OBJECT_UPDATE": true
      }
    }
  ],
  "existingObjects": 0,
  "maximumObjects": 0,
  "additionalExistingObjects": 0,
  "additionalMaximumObjects": 0
}
```

---

### `GET` /api/requirement/{id}

**Find Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "customPropertyValues": {
    "1": [
      "string"
    ],
    "2": [
      "string"
    ]
  },
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

---

### `DELETE` /api/requirement/{id}

**Delete Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `DELETE` /api/requirement/async/{id}

**Delete an object asynchronously (returns a Job ID)**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example** (Asynchronous Job)

```json
{
  "id": 0,
  "status": "COMPLETED",
  "startTime": "2026-02-26T04:37:56.982Z",
  "endTime": "2026-02-26T04:37:56.982Z"
}
```

---

## Status Value

Manage Status Value objects — workflow status values used across glossary objects.

### `PUT` /api/status

**Update Object**

**Parameters**

No parameters.
**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `POST` /api/status

**Create Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "defaultIndicator": true,
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "defaultIndicator": true,
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

---

### `POST` /api/status/search

**Search Objects**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "startFrom": 0,
  "maxResults": 0,
  "filters": [
    {
      "type": "SIMPLE_QUERY",
      "property": "string",
      "value": "string",
      "timezone": "string",
      "relationType": "RELATED_TO"
    }
  ],
  "sort": {
    "type": "ASCENDING",
    "property": "string"
  },
  "asOfTime": 0
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "size": 0,
  "rows": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
      "changedBy": {
        "id": 0,
        "name": "string"
      },
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "chips": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "defaultIndicator": true,
      "childrenCounts": {
        "id": 0,
        "type": "string",
        "domainsCount": 0,
        "domainOwnersCount": 0,
        "dataStewardsCount": 0,
        "dataAssetsCount": 0,
        "dataSetsCount": 0,
        "dataStructuresCount": 0,
        "dataFieldsCount": 0,
        "businessTermsCount": 0,
        "entitiesCount": 0,
        "referenceAttributeTargetEntitiesCount": 0,
        "attributesCount": 0,
        "calculationRulesCount": 0,
        "attributeDefinitionsCount": 0,
        "compositeTypesCount": 0,
        "customPropertiesCount": 0,
        "businessRulesCount": 0,
        "businessModelMappingsCount": 0,
        "processesCount": 0,
        "processStepsCount": 0,
        "processMappingsCount": 0,
        "technicalDataMappingsCount": 0,
        "commentsCount": 0,
        "objectType": "string"
      },
      "activeNotifications": {
        "COMMENT_UPDATE": true,
        "OBJECT_UPDATE": true
      }
    }
  ],
  "existingObjects": 0,
  "maximumObjects": 0,
  "additionalExistingObjects": 0,
  "additionalMaximumObjects": 0
}
```

---

### `GET` /api/status/{id}

**Find Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "defaultIndicator": true,
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

---

### `DELETE` /api/status/{id}

**Delete Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `DELETE` /api/status/async/{id}

**Delete an object asynchronously (returns a Job ID)**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example** (Asynchronous Job)

```json
{
  "id": 0,
  "status": "COMPLETED",
  "startTime": "2026-02-26T04:37:57.026Z",
  "endTime": "2026-02-26T04:37:57.026Z"
}
```

---

## Technical Data Mapping

Manage Technical Data Mapping objects — mappings between technical data elements.

### `PUT` /api/technical-data-mapping

**Update Object**

**Parameters**

No parameters.
**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `POST` /api/technical-data-mapping

**Create Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "baseDataSet": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string",
    "dataSetType": "Logical",
    "dataSetDomains": [
      {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    ],
    "dataSource": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSourceType": "ACCURITY_EDGE_PULL"
    }
  },
  "technicalDataMappingBaseDataStructureDataFields": [
    {
      "id": 0,
      "dataStructure": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "dataField": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "operation": "string",
      "objectType": "string"
    }
  ],
  "technicalDataMappingBaseSelectionItems": [
    {
      "id": 0,
      "dataStructure": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "st
  // ... (truncated for brevity)
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "baseDataSet": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string",
    "dataSetType": "Logical",
    "dataSetDomains": [
      {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    ],
    "dataSource": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSourceType": "ACCURITY_EDGE_PULL"
    }
  },
  "technicalDataMappingBaseDataStructureDataFields": [
    {
      "id": 0,
      "dataStructure": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "dataField": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "operation": "string",
      "objectType": "string"
    }
  ],
  "technicalDataMappingBaseSelectionItems": [
    {
      "id": 0,
      "dataStructure": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "st
  // ... (truncated for brevity)
```

---

### `POST` /api/technical-data-mapping/search

**Search Objects**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "startFrom": 0,
  "maxResults": 0,
  "filters": [
    {
      "type": "SIMPLE_QUERY",
      "property": "string",
      "value": "string",
      "timezone": "string",
      "relationType": "RELATED_TO"
    }
  ],
  "sort": {
    "type": "ASCENDING",
    "property": "string"
  },
  "asOfTime": 0
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "size": 0,
  "rows": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
      "changedBy": {
        "id": 0,
        "name": "string"
      },
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "chips": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "tags": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "status": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "baseDataSet": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string",
        "dataSetType": "Logical",
        "dataSetDomains": [
          {
            "id": 0,
            "name": "string",
            "description": {
              "plainTextValue": "string",
              "formattedValue": "string"
            },
            "objectType": "string"
          }
        ],
        "dataSource": {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string",
          "dataSourceType": "ACCURITY_EDGE_PULL"
        }
      },
      "technicalDataMappingBaseDataStructureDataFields": [
        {
          "id": 0,
          "dataStructure": {
            "id": 0,
            "name": "string",
            "description": {
              "plainTextValue": "string",
              "formattedValue": "string"
            },
            "objectType": "string"
          },
          "dataField": {
            "id": 0,
            "name": "string",
            "description": {
              "plainTex
  // ... (truncated for brevity)
```

---

### `GET` /api/technical-data-mapping/{id}

**Find Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "tags": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "status": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string"
  },
  "baseDataSet": {
    "id": 0,
    "name": "string",
    "description": {
      "plainTextValue": "string",
      "formattedValue": "string"
    },
    "objectType": "string",
    "dataSetType": "Logical",
    "dataSetDomains": [
      {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      }
    ],
    "dataSource": {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string",
      "dataSourceType": "ACCURITY_EDGE_PULL"
    }
  },
  "technicalDataMappingBaseDataStructureDataFields": [
    {
      "id": 0,
      "dataStructure": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "dataField": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "string"
        },
        "objectType": "string"
      },
      "operation": "string",
      "objectType": "string"
    }
  ],
  "technicalDataMappingBaseSelectionItems": [
    {
      "id": 0,
      "dataStructure": {
        "id": 0,
        "name": "string",
        "description": {
          "plainTextValue": "string",
          "formattedValue": "st
  // ... (truncated for brevity)
```

---

### `DELETE` /api/technical-data-mapping/{id}

**Delete Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `DELETE` /api/technical-data-mapping/async/{id}

**Delete an object asynchronously (returns a Job ID)**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example** (Asynchronous Job)

```json
{
  "id": 0,
  "status": "COMPLETED",
  "startTime": "2026-02-26T04:37:57.088Z",
  "endTime": "2026-02-26T04:37:57.088Z"
}
```

---

## Value Type

Manage Value Type objects — type definitions for attribute values.

### `PUT` /api/value-type

**Update Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

---

### `POST` /api/value-type

**Create Object**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

---

### `POST` /api/value-type/search

**Search Objects**

**Parameters**

No parameters.
**Request Body** (Content-Type: `application/json`)

```json
{
  "startFrom": 0,
  "maxResults": 0,
  "filters": [
    {
      "type": "SIMPLE_QUERY",
      "property": "string",
      "value": "string",
      "timezone": "string",
      "relationType": "RELATED_TO"
    }
  ],
  "sort": {
    "type": "ASCENDING",
    "property": "string"
  },
  "asOfTime": 0
}
```

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "size": 0,
  "rows": [
    {
      "id": 0,
      "version": 0,
      "name": "string",
      "objectType": "string",
      "createdDate": 0,
      "changedDate": 0,
      "createdBy": {
        "id": 0,
        "name": "string"
      },
      "changedBy": {
        "id": 0,
        "name": "string"
      },
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "chips": [
        {
          "id": 0,
          "name": "string",
          "description": {
            "plainTextValue": "string",
            "formattedValue": "string"
          },
          "objectType": "string"
        }
      ],
      "childrenCounts": {
        "id": 0,
        "type": "string",
        "domainsCount": 0,
        "domainOwnersCount": 0,
        "dataStewardsCount": 0,
        "dataAssetsCount": 0,
        "dataSetsCount": 0,
        "dataStructuresCount": 0,
        "dataFieldsCount": 0,
        "businessTermsCount": 0,
        "entitiesCount": 0,
        "referenceAttributeTargetEntitiesCount": 0,
        "attributesCount": 0,
        "calculationRulesCount": 0,
        "attributeDefinitionsCount": 0,
        "compositeTypesCount": 0,
        "customPropertiesCount": 0,
        "businessRulesCount": 0,
        "businessModelMappingsCount": 0,
        "processesCount": 0,
        "processStepsCount": 0,
        "processMappingsCount": 0,
        "technicalDataMappingsCount": 0,
        "commentsCount": 0,
        "objectType": "string"
      },
      "activeNotifications": {
        "COMMENT_UPDATE": true,
        "OBJECT_UPDATE": true
      }
    }
  ],
  "existingObjects": 0,
  "maximumObjects": 0,
  "additionalExistingObjects": 0,
  "additionalMaximumObjects": 0
}
```

---

### `GET` /api/value-type/{id}

**Find Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example**

```json
{
  "id": 0,
  "version": 0,
  "name": "string",
  "objectType": "string",
  "createdDate": 0,
  "changedDate": 0,
  "createdBy": {
    "id": 0,
    "name": "string"
  },
  "changedBy": {
    "id": 0,
    "name": "string"
  },
  "description": {
    "plainTextValue": "string",
    "formattedValue": "string"
  },
  "chips": [
    {
      "id": 0,
      "name": "string",
      "description": {
        "plainTextValue": "string",
        "formattedValue": "string"
      },
      "objectType": "string"
    }
  ],
  "childrenCounts": {
    "id": 0,
    "type": "string",
    "domainsCount": 0,
    "domainOwnersCount": 0,
    "dataStewardsCount": 0,
    "dataAssetsCount": 0,
    "dataSetsCount": 0,
    "dataStructuresCount": 0,
    "dataFieldsCount": 0,
    "businessTermsCount": 0,
    "entitiesCount": 0,
    "referenceAttributeTargetEntitiesCount": 0,
    "attributesCount": 0,
    "calculationRulesCount": 0,
    "attributeDefinitionsCount": 0,
    "compositeTypesCount": 0,
    "customPropertiesCount": 0,
    "businessRulesCount": 0,
    "businessModelMappingsCount": 0,
    "processesCount": 0,
    "processStepsCount": 0,
    "processMappingsCount": 0,
    "technicalDataMappingsCount": 0,
    "commentsCount": 0,
    "objectType": "string"
  },
  "activeNotifications": {
    "COMMENT_UPDATE": true,
    "OBJECT_UPDATE": true
  }
}
```

---

### `DELETE` /api/value-type/{id}

**Delete Object**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

---

### `DELETE` /api/value-type/async/{id}

**Delete an object asynchronously (returns a Job ID)**

**Parameters**

| Name | In | Type | Required |
|------|----|------|----------|
| `id` | path | `integer($int64)` | Yes |

**Responses**

| Code | Description |
|------|-------------|
| 200 | OK |

**Response Body Example** (Asynchronous Job)

```json
{
  "id": 0,
  "status": "COMPLETED",
  "startTime": "2026-02-26T04:37:57.142Z",
  "endTime": "2026-02-26T04:37:57.142Z"
}
```

---

## API Version Information

- **API Version:** 1.22.17
- **OpenAPI Specification:** OAS3
- **Base URL:** `https://app.accurity.ai`
- **API Docs Endpoint:** `/v3/api-docs/default`

## Error Handling

The API returns standard HTTP status codes:

| Code | Meaning |
|------|--------|
| 200 | Success |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource does not exist |
| 500 | Internal Server Error |
