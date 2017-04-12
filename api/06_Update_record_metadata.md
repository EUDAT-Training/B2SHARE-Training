# Update record metadata
In this guide the addition and editing of metadata of both published and draft records is explained. In many cases the metadata fields and values of draft or published records need to be changed in order to correct small mistakes or add missing metadata fields.

Please note that altering the metadata of a published record will generate a new version of that record with new PIDs and checksums. The original version of the record will always be discoverable and citeable with its own PID, unless it is taken offline.

This guide covers:

- Getting metadata schema information
- Preparing new metadata
- Creating a JSON patch
- Submitting your patch
- Inspecting the result

Refer to [Request and Metadata Reference Guide](B_Request_and_Metadata_Reference_Guide.md) to get the required and optional list of fields used for metadata.

In this guide a draft record with ID `b43a0e6914e34de8bd19613bcdc0d364` will be updated, so this number will be used during each step. Any modifications to metadata should be done to the record's draft equivalent. This object is found by adding the `draft` endpoint.

## Getting metadata schema information
Every record is published as part of a community. Each community has specific metadata schemas designed to cover the necessary information in order to easily understand and assess the contents of a publication. If an update needs to be made to the metadata fields and/or values, first the community's metadata schema needs to be examined to understand which fields can be added or updated.

Lets determine the draft record's community ID as stored in its metadata:

```python
>>> recordid = 'b43a0e6914e34de8bd19613bcdc0d364'
>>> url = "https://trng-b2share.eudat.eu/api/records/" + recordid + "/draft"
>>> r = requests.get(url, params={'access_token': token})
>>> result = json.loads(r.text)
>>> print result["metadata"]["community"]
e9b9792e-79fb-4b07-b6b4-b9c2bd06d095
```

With this community ID, the community metadata schema can be retrieved and required metadata fields listed. Refer to the [Get community metadata schema](03_Communities.md#get-community-metadata-schema) section of the [Communities](03_Communities.md) guide to see how to achieve this.

## Updating metadata
To update a draft record's metadata, the record ID is required while making patch requests. The procedure can be applied to either draft or published records.

#### Preparing your new metadata
An object with the new and updated metadata fields and values needs to be constructed. As the community, title and open access check have already been set when the draft record was created, only some missing fields are provided:

```python
>>> metadata = {"creators": "B2SHARE-Training author",
                "description": "My first dataset ingested using the B2SHARE API",
                "licence": "CC-0-BY",
                "contact_email": "email@example.com"}
```

#### Creating a JSON patch
The metadata update call is made using a patch request containing the patch operations and headers. Note that:

- The `api/records/<record_id>/draft` API end-point is used
- The metadata updates for the record must be provided in the [JSON patch format](http://jsonpatch.com) in order to avoid to have to send all the existing metadata as well
- The patch format contains one or more JSONPath strings. The root of these paths is the metadata object, as this is the only mutable object

In order to successfully update the metadata, a JSON patch is created using the `jsonpatch` Python package. First, the original existing metadata of the record is retrieved which will later be altered:

```python
>>> url = "https://trng-b2share.eudat.eu/api/records/" + recordid
>>> r = requests.get(url, params=payload)
>>> result = json.loads(r.text)
>>> metadata_old = result["metadata"]
>>> print json.dumps(metadata_old, indent=4)
{
    "community_specific": {},
    "publication_state": "draft",
    "owners": [
        10
    ],
    "open_access": true,
    "community": "e9b9792e-79fb-4b07-b6b4-b9c2bd06d095",
    "titles": [
        {
            "title": "My test upload"
        }
    ],
    "$schema": "https://trng-b2share.eudat.eu/api/communities/e9b9792e-79fb-4b07-b6b4-b9c2bd06d095/schemas/0#/draft_json_schema"
}
```

The actual JSON patch is created by:

```python
>>> import jsonpatch
>>> patch = jsonpatch.make_patch(metadata_old, metadata)
>>> print patch
[{"path": "/community_specific", "op": "remove"}, {"path": "/publication_state", "op": "remove"}, {"path": "/owners", "op": "remove"}, {"path": "/open_access", "op": "remove"}, {"path": "/community", "op": "remove"}, {"path": "/titles", "op": "remove"}, {"path": "/$schema", "op": "remove"}, {"path": "/publisher", "value": "EUDAT", "op": "add"}, {"path": "/contact_email", "value": "email@example.com", "op": "add"}, {"path": "/descriptions", "value": [{"description": "My first dataset ingested using the B2SHARE API", "description_type": "Abstract"}], "op": "add"}, {"path": "/language", "value": "en_GB", "op": "add"}]
```

The current patch will remove any existing fields not present in the new metadata object, therefore these need to be removed in the final patch:

```python
>>> finpatch = filter(lambda x: x["op"] <> "remove", patch)
>>> print finpatch
[{u'path': u'/publisher', u'value': 'EUDAT', u'op': u'add'}, {u'path': u'/contact_email', u'value': 'email@example.com', u'op': u'add'}, {u'path': u'/descriptions', u'value': [{'description': 'My first dataset ingested using the B2SHARE API', 'description_type': 'Abstract'}], u'op': u'add'}, {u'path': u'/language', u'value': 'en_GB', u'op': u'add'}]
```

The patch needs to be provided to the `data` argument as a serialized string for which the JSON package can be used:

```python
>>> strpatch = json.dumps(finpatch)
>>> print strpatch
[{"path": "/publisher", "value": "EUDAT", "op": "add"}, {"path": "/contact_email", "value": "email@example.com", "op": "add"}, {"path": "/descriptions", "value": [{"description": "My first dataset ingested using the B2SHARE API", "description_type": "Abstract"}], "op": "add"}, {"path": "/language", "value": "en_GB", "op": "add"}]
```

#### Submitting the patch
The serialized JSON patch is sent to the service in order to update the metadata.

First, the request headers need to be defined:

```python
>>> header = {'Content-Type': 'application/json-patch+json'}
```

Now, the request response text shows the updated metadata:

```python
>>> url = 'https://trng-b2share.eudat.eu/api/records/' + recordid + "/draft"
>>> r = requests.patch(url, data=strpatch, params=payload, headers=header)
>>> print r
<Response [200]>
>>> result = json.loads(r.text)
>>> print json.dumps(result, indent=4)
{
    "updated": "2017-03-02T17:03:37.500387+00:00",
    "metadata": {
        "community_specific": {},
        "publication_state": "draft",
        "open_access": true,
        "language": "en_GB",
        "publisher": "EUDAT",
        "owners": [
            10
        ],
        "community": "e9b9792e-79fb-4b07-b6b4-b9c2bd06d095",
        "titles": [
            {
                "title": "My test upload"
            }
        ],
        "contact_email": "email@example.com",
        "descriptions": [
            {
                "description": "My first dataset ingested using the B2SHARE API",
                "description_type": "Abstract"
            }
        ],
        "$schema": "https://trng-b2share.eudat.eu/api/communities/e9b9792e-79fb-4b07-b6b4-b9c2bd06d095/schemas/0#/draft_json_schema"
    },
    "id": "b43a0e6914e34de8bd19613bcdc0d364",
    "links": {
        "files": "https://trng-b2share.eudat.eu/api/files/0163d244-5845-40ca-899c-d1d0025f68aa",
        "self": "https://trng-b2share.eudat.eu/api/records/b43a0e6914e34de8bd19613bcdc0d364/draft",
        "publication": "https://trng-b2share.eudat.eu/api/records/b43a0e6914e34de8bd19613bcdc0d364"
    },
    "created": "2017-03-02T16:34:26.383505+00:00"
}
```

Compare the created and updated metadata timestamp:

```python
>>> print result["created"], result["updated"]
2017-03-02T16:34:26.383505+00:00 2017-03-02T17:03:37.500387+00:00
```

In case the patch request did not succeed (status code 400), an error description containing all errors is returned in the request response text. For example, the `creators` field value needs to be an array:

```python
>>> patch = '[{"path": "/creators", "value": "B2SHARE-Training author", "op": "add"}]'
>>> r = requests.patch(url, data=patch, params=payload, headers=header)
>>> print r.status_code
400
>>> print r.text
{"message": "Validation error.", "status": 400, "errors": [{"message": "'B2SHARE-Training author' is not of type 'array'", "field": "creators"}]}
```

## Updating all community metadata fields
If you are publishing datasets as part of specific communities, often all metadata fields that the community specifies in the community metadata schema need to be provided upon commit. For a strategy to achieve this, please follow the next [Update all community metadata fields](07_Update_all_community_metadata_fields.md) guide.
