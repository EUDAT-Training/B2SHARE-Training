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
>>> r = requests.get('https://trng-b2share.eudat.eu/api/communities')
>>> result = json.loads(r.text)
>>> print(json.dumps(result["hits"]["hits"][5], indent=4))
{
    "updated": "Wed, 21 Dec 2016 08:57:40 GMT",
    "name": "EUDAT",
    "links": {
        "self": "https://trng-b2share.eudat.eu/api/communities/e9b9792e-79fb-4b07-b6b4-b9c2bd06d095"
    },
    "created": "Wed, 21 Dec 2016 08:57:40 GMT",
    "publication_workflow": "direct_publish",
    "restricted_submission": false,
    "roles": {
        "admin": {
            "description": "Admin role of the community \"EUDAT\"",
            "name": "com:e9b9792e79fb4b07b6b4b9c2bd06d095:admin",
            "id": 11
        },
        "member": {
            "description": "Member role of the community \"EUDAT\"",
            "name": "com:e9b9792e79fb4b07b6b4b9c2bd06d095:member",
            "id": 12
        }
    },
    "logo": "/img/communities/eudat.png",
    "id": "e9b9792e-79fb-4b07-b6b4-b9c2bd06d095",
    "description": "The big Eudat community. Use this community if no other is suited for you"
}
```

The total number of defined communities is found in the `total` key:

```python
>>> print(result["hits"]["total"])
11
```

The community identifier can be found by:

```python
>>> community_id = result["hits"]["hits"][5]["id"]
>>> print(community_id)
e9b9792e-79fb-4b07-b6b4-b9c2bd06d095
```

## Retrieve community-specific records
If you solely want the records of a given community, say EUDAT, the corresponding community identifier must be added to the records request as part of the query parameter `q`. Using the information found in the previous section:

```python
>>> params = {'q': 'community:' + community_id}
>>> r = requests.get('https://trng-b2share.eudat.eu/api/records', params=params)
```

By repeating the processing with JSON, the number of results can be displayed:

```python
>>> result = json.loads(r.text)
>>> print(result["hits"]["total"])
94
```

The structure of the results is exactly the same as with other records-retrieving requests:

```python
>>> print(json.dumps(result["hits"]["hits"][0], indent=4))
{
    "files": [
        {
            "checksum": "md5:098f6bcd4621d373cade4e832627b4f6",
            "bucket": "b425ea3a-7c9a-463c-bf59-2b740951eed4",
            "ePIC_PID": "http://hdl.handle.net/11304/a2f3323a-b692-4a94-b7cd-21f548feaa7b",
            "version_id": "fca556c1-aeb3-469f-be81-47b3c100f39f",
            "key": "TestFileToBeUploaded.txt",
            "size": 4
        }
    ],
    "updated": "2017-01-03T08:39:26.514585+00:00",
    "links": {
        "files": "https://trng-b2share.eudat.eu/api/files/b425ea3a-7c9a-463c-bf59-2b740951eed4",
        "self": "https://trng-b2share.eudat.eu/api/records/0181d55ac4654a148357ca16452e3ef5"
    },
    "created": "2017-01-03T08:39:26.514576+00:00",
    "id": "0181d55ac4654a148357ca16452e3ef5",
    "metadata": {
        "community_specific": {},
        "publication_state": "published",
        "open_access": true,
        "ePIC_PID": "http://hdl.handle.net/11304/4104e1db-c3f7-4d01-9fcd-d00c8b1c3175",
        "community": "e9b9792e-79fb-4b07-b6b4-b9c2bd06d095",
        "titles": [
            {
                "title": "2794dbfd-4bf2-4b1b-a084-32c574ad258a"
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

If an empty community collection is requested, the response will be positive, but the results structure will be empty.

## Get community metadata schema
Each community has a specific metadata schema which identifies all the fields that possibly need to be filled in before a new record can be completed.

Schema definition are defined using the [JSON Schema specification](http://json-schema.org/documentation.html) that allows automatic validation of all fields according the schema. The specification currently has Internet-Draft status and is reviewed by the Internet Engineering Task Force (IETF). For a more elaborate description, refer to the [Data Structures](../deploy/10_Data_structures.md) guide in the deploy module of this repository.

To retrieve the community metadata schema, use the `/api/communities/<community_id>/schemas/<version>` API endpoint. The `version` parameter can be a number or, to get the latest version, 'last'.

```python
>>> r = requests.get('https://trng-b2share.eudat.eu/api/communities/e9b9792e-79fb-4b07-b6b4-b9c2bd06d095/schemas/last')
>>> result = json.loads(r.text)
>>> print(json.dumps(result["json_schema"], indent=4))
{
    "allOf": [
        {
            "b2share": {
                "presentation": {
                    "major": [
                        "community",
                        "titles",
                        ...
                        "contact_email"
                    ],
                    "minor": [
                        "contributors",
                        ...
                        "language"
                    ]
                }
            },
            "required": [
                "community",
                "titles",
                "open_access",
                "publication_state",
                "community_specific"
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
                "contributors": {
                    "uniqueItems": true,
                    "items": {
                        "additionalProperties": false,
                        "required": [
                            "contributor_name",
                            "contributor_type"
                        ],
                        "type": "object",
                        "properties": {
                            "contributor_name": {
                                "type": "string",
                                "title": "Name"
                            },
                            "contributor_type": {
                                "enum": [
                                    "ContactPerson",
                                    ...
                                    "Other"
                                ],
                                "title": "Type"
                            }
                        }
                    },
                    "type": "array",
                    "description": "The list of all other contributors. Please mention all persons that were relevant in the creation of the resource.",
                    "title": "Contributors"
                },
                "community": {
                    "type": "string",
                    "description": "The community to which the record has been submitted.",
                    "title": "Community"
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

Please note that several listings have been shortened for clarity.

The schema contains all required fields together with field type and descriptions. The required fields are also listed and need to be provided in case new records are created. The definition is used by B2SHARE to validate the metadata schema values you provide.

To fully process a metadata schema definition during the metadata annotation phase of the ingest workflow, refer to the [Update all community metadata fields](07_Update_all_community_metadata_fields.md) guide.

## Registering new communities
It is possible to register new communities in B2SHARE, but currently not via the API. Please contact the [EUDAT helpdesk](https://eudat.eu/support-request?service=B2SHARE) in order to do so. If you are using your own instance of B2SHARE, you can configure a community directly using the provided tools. Refer to the [Community Integration](../deploy/12_Community_integration.md) guide of the [B2SHARE Deployment](../deploy) module on how to do this.
