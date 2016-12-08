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
>>> r = requests.get('https://vm0045.kaj.pouta.csc.fi/api/communities', params={'access_token': token}, verify=False)
>>> result = json.loads(r.text)
>>> print json.dumps(result["hits"]["hits"][5], indent=4)
{
    "updated": "Wed, 16 Nov 2016 10:23:21 GMT",
    "name": "EUDAT",
    "links": {
        "self": "https://vm0045.kaj.pouta.csc.fi/api/communities/e9b9792e-79fb-4b07-b6b4-b9c2bd06d095"
    },
    "created": "Wed, 16 Nov 2016 10:23:21 GMT",
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
>>> payload = {'q': 'community:e9b9792e-79fb-4b07-b6b4-b9c2bd06d095',
               'access_token': token
               }
>>> r = requests.get('https://vm0045.kaj.pouta.csc.fi/api/records', params=payload, verify=False)
```

By repeating the processing with JSON, the number of results can be displayed:
```python
>>> result = json.loads(r.text)
>>> print result["hits"]["total"]
286
```

The structure of the results is exactly the same as with other records-retrieving requests:
```python
>>> print json.dumps(result["hits"]["hits"][1], indent=4)
{
    "files": [
        {
            "checksum": "md5:4f643f1dea4a2db45d89432659614bf1",
            "bucket": "481c287f-ee1a-4856-b8ef-385c92c14a89",
            "ePIC_PID": "http://hdl.handle.net/11304/0739469b-e4d9-4a03-8e59-1e0aa2f37025",
            "version_id": "92091101-a459-48f2-bfb4-fdc1c24bf278",
            "key": "ColonyArea.zip",
            "size": 9486352
        },
        ...
    ],
    "updated": "2016-11-16T10:29:26.365842+00:00",
    "links": {
        "files": "https://vm0045.kaj.pouta.csc.fi/api/files/481c287f-ee1a-4856-b8ef-385c92c14a89",
        "self": "https://vm0045.kaj.pouta.csc.fi/api/records/ce33c120b0a44a8e846c6080a024d943"
    },
    "created": "2016-11-16T10:29:26.365834+00:00",
    "id": "ce33c120b0a44a8e846c6080a024d943",
    "metadata": {
        "publication_state": "published",
        "open_access": true,
        "DOI": "10.5072/b2share.14553461-fae4-49f3-8c2b-b0b89b0f83dd",
        "description": "Clonogenic assays ... each file.",
        "contributors": [],
        "title": "ImageJ plugin ColonyArea",
        "owners": [
            10
        ],
        "ePIC_PID": "http://hdl.handle.net/11304/ff311171-e830-4bf4-842c-14e3c822c9e0",
        "community": "e9b9792e-79fb-4b07-b6b4-b9c2bd06d095",
        "contact_email": "",
        "keywords": [],
        "alternate_identifier": "http://hdl.handle.net/11304/3522daa6-b988-11e3-8cd7-14feb57d12b9",
        "$schema": "https://vm0045.kaj.pouta.csc.fi/api/communities/e9b9792e-79fb-4b07-b6b4-b9c2bd06d095/schemas/0#/json_schema",
        "resource_type": []
    }
}
```

Each record is identical in structure as in the other requests. If an empty community collection is requested, the response will be positive, but the results structure will be empty:
```python
>>> r = requests.get('https://trng-b2share.eudat.eu/api/records/bbmri', params=payload, verify=False)
>>> result = json.loads(r.text)
>>> print result["hits"]["hits"]
```

## Get community metadata schema
Each community has a specific metadata schema specified which identifies all the fields that possibly need to be filled in before a new record can be completed.

To retrieve the community metadata schema, use the `/api/communities/<community_id>/schemas/<version>` API endpoint. The `version` parameter can be a number or, to get the latest version, 'last'.
```python
>>> r = requests.get('https://vm0045.kaj.pouta.csc.fi/api/communities/e9b9792e-79fb-4b07-b6b4-b9c2bd06d095/schemas/last', params=payload, verify=False)
>>> print json.dumps(result["json_schema"], indent=4)
{
    "allOf": [
        {
            "b2share": {
                "presentation": {
                    "major": [
                        "community",
                        "title",
                        "description",
                        "creators",
                        "open_access",
                        "licence",
                        "keywords",
                        "contact_email",
                        "discipline"
                    ],
                    "minor": [
                        "contributors",
                        "resource_type",
                        "alternate_identifier",
                        "version",
                        "publisher",
                        "language"
                    ]
                }
            },
            "required": [
                "community",
                "title",
                "open_access"
            ],
            "additionalProperties": false,
            "$schema": "http://json-schema.org/draft-04/schema#",
            "type": "object",
            "properties": {
                "embargo_date": {
                    "title": "Embargo Date",
                    "type": "string",
                    "description": "The date ... access.",
                    "format": "date-time"
                },
                "contributors": {
                    "uniqueItems": true,
                    "items": {
                        "type": "string"
                    },
                    "type": "array",
                    "description": "The list ... resource.",
                    "title": "Contributors"
                },
                "community": {
                    "type": "string",
                    "description": "The community to which the record has been submitted.",
                    "title": "Community"
                },
                ...
                "resource_type": {
                    "uniqueItems": true,
                    "items": {
                        "enum": [
                            "Audiovisual",
                            ...
                            "Other"
                        ],
                        "type": "string"
                    },
                    "type": "array",
                    "description": "The type of the resource.",
                    "title": "Resource Type"
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

The schema contains all required fields together with field type and descriptions.

## Registering new communities
It is possible to register new communities in B2SHARE, but currently not via de the API. Please contact the [EUDAT helpdesk](https://eudat.eu/support-request?service=B2SHARE) in order to do so.
