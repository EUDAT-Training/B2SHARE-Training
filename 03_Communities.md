# Communities
B2SHARE places records in community-specific collections. A user can only retrieve information about existing, already registered communities. To register new communities and define community-specific metadata schemas please refer to [dedicated](#registering-new-communities) section. This guide covers:

- Retrieval a list of all available communities
- Retrieval of community specific information
- Retrieval of a community's metadata schema

### Setup your connection
Please make sure your machine has been properly set up to use Python and required packages. Follow [this](A_Setup_and_install.md) guide in order to do so.

This guide assumes you have successfully registered your account on the [B2SHARE website](https://trng-b2share.eudat.eu) using your institutional credentials or social ID through B2ACCESS. In addition, the loading of the token, importing Python packages and checking request responses will not be covered here.

## List communities
To assess which communities are defined in B2SHARE, use the communities API end-point `/api/communities`. By default, B2SHARE returns all defined communities when requested. To see information about the EUDAT community (at index 5), do as follows:

```python
>>> r = requests.get('https://trng-b2share.eudat.eu/api/communities', verify=False)
>>> result = json.loads(r.text)
>>> print json.dumps(result["hits"]["hits"][5], indent=4)
{
    "updated": "Wed, 21 Dec 2016 08:57:40 GMT",
    "name": "EUDAT",
    "links": {
        "self": "https://trng-b2share.eudat.eu/api/communities/e9b9792e-79fb-4b07-b6b4-b9c2bd06d095"
    },
    "created": "Wed, 21 Dec 2016 08:57:40 GMT",
    "publication_workflow": "direct_publish",
    "restricted_submission": false,
    "logo": "/img/communities/eudat.png",
    "id": "e9b9792e-79fb-4b07-b6b4-b9c2bd06d095",
    "description": "The big Eudat community. Use this community if no other is suited for you"
}
```

The total number of defined communities is found in the `total` key:

```python
>>> print result["hits"]["total"]
11
```

## Retrieve community-specific records
If you solely want the records of a given community, say EUDAT, the corresponding community ID must be added to the records request as part of the query parameter `q`. Using the information found in the previous section:

```python
>>> payload = {'q': 'community:4ba7c0fd-1435-4313-9c13-4d888d60321a'}
>>> r = requests.get('https://trng-b2share.eudat.eu/api/records', params=payload, verify=False)
```

By repeating the processing with JSON, the number of results can be displayed:
```python
>>> result = json.loads(r.text)
>>> print result["hits"]["total"]
19
```

The structure of the results is exactly the same as with other records-retrieving requests:
```python
>>> print json.dumps(result["hits"]["hits"][1], indent=4)
{
    "files": [
        {
            "checksum": "md5:098f6bcd4621d373cade4e832627b4f6",
            "bucket": "f5069510-bc1b-4b94-9bc6-8e6bc52c7c36",
            "ePIC_PID": "http://hdl.handle.net/11304/9ea8bd93-611e-4c64-a1f0-d51876bfa5b6",
            "version_id": "069addf7-11b4-40bd-8b75-431d83f99b3f",
            "key": "TestFileToBeUploaded.txt",
            "size": 4
        }
    ],
    "updated": "2017-01-03T09:49:24.063303+00:00",
    "links": {
        "files": "https://trng-b2share.eudat.eu/api/files/f5069510-bc1b-4b94-9bc6-8e6bc52c7c36",
        "self": "https://trng-b2share.eudat.eu/api/records/7cef0c46e0424ca4be0ef6d4574fae2d"
    },
    "created": "2017-01-03T09:49:24.063293+00:00",
    "id": "7cef0c46e0424ca4be0ef6d4574fae2d",
    "metadata": {
        "community_specific": {},
        "publication_state": "published",
        "open_access": true,
        "ePIC_PID": "http://hdl.handle.net/11304/4f48476f-bb46-432f-bd39-d50f2fd26b32",
        "community": "e9b9792e-79fb-4b07-b6b4-b9c2bd06d095",
        "titles": [
            {
                "title": "61121cde-982c-4684-b83d-b1ebb819e73d"
            }
        ],
        "keywords": [
            "keyword1",
            "keyword2"
        ],
        "owners": [
            3
        ],
        "$schema": "https://trng-b2share.eudat.eu/api/communities/e9b9792e-79fb-4b07-b6b4-b9c2bd06d095/schemas/0#/json_schema"
    }
}
```

Each record is identical in structure as in the other requests. If an empty community collection is requested, the response will be positive, but the results structure will be empty.

## Get community metadata schema
Each community has a specific metadata schema specified which identifies all the fields that possibly need to be filled in before a new record can be completed.

To retrieve the community metadata schema, use the `/api/communities/<community_id>/schemas/<version>` API endpoint. The `version` parameter can be a number or, to get the latest version, 'last'.
```python
>>> r = requests.get('https://trng-b2share.eudat.eu/api/communities/e9b9792e-79fb-4b07-b6b4-b9c2bd06d095/schemas/last', params=payload, verify=False)
>>> result = json.loads(r.text)
>>> print json.dumps(result["json_schema"], indent=4)
{
    "allOf": [
        {
            "b2share": {
                "presentation": {
                    "major": [
                        "community",
                        ...
                    ],
                    "minor": [
                        "contributors",
                        ...
                    ]
                }
            },
            "required": [
                "community",
                ...
            ],
            "additionalProperties": false,
            "$schema": "http://json-schema.org/draft-04/schema#",
            "type": "object",
            "properties": {
                "embargo_date": {
                    "title": "Embargo Date",
                    "type": "string",
                    "description": "The date marking the end of the embargo period. The record will be marked as open access on the specified date at midnight. Please note that the record metadata is always publicly accessible, and only the data files can have private access.",
                    "format": "date-time"
                },
                ...
                "creators": {
                    "uniqueItems": true,
                    "items": {
                        "additionalProperties": false,
                        "required": [
                            "creator_name"
                        ],
                        "type": "object",
                        "properties": {
                            "creator_name": {
                                "type": "string"
                            }
                        }
                    },
                    "type": "array",
                    "description": "The full name of the creators. The personal name format should be: family, given (e.g.: Smith, John).",
                    "title": "Creators"
                }
            }
        },
        {
            "type": "object",
            "properties": {
                "community_specific": {
                    "additionalProperties": false,
                    "$schema": "http://json-schema.org/draft-04/schema#",
                    "type": "object",
                    "properties": {}
                }
            }
        }
    ]
}
```

The schema contains all required fields together with field type and descriptions. The required fields are also listed and need to be provided in case new records are created.

## Registering new communities
It is possible to register new communities in B2SHARE, but currently not via the API. Please contact the [EUDAT helpdesk](https://eudat.eu/support-request?service=B2SHARE) in order to do so.
