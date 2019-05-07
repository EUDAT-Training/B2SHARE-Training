# Update record metadata
In this guide the addition and editing of metadata of both published and draft records is explained. In many cases the metadata fields and values of draft or published records need to be changed in order to correct small mistakes or add missing metadata fields.

Please note that altering the metadata of a published record will generate a new version of that record with new PIDs and checksums. The original version of the record will always be discoverable and citeable with its own PID, unless it is taken offline.

This guide covers:
- Metadata update concepts
- Getting metadata schema information
- Preparing new metadata
- Creating a JSON patch
- Submitting your patch
- Inspecting the result
- Updating community-specific metadata fields
- Updating multivalue metadata fields

Refer to [Request and Metadata Reference Guide](B_Request_and_Metadata_Reference_Guide.md) to get the required and optional list of fields used for metadata.

In this guide a draft record with identifier `b43a0e6914e34de8bd19613bcdc0d364` will be updated, so this number will be used during each step. Any modifications to metadata should be done to the record's draft equivalent. This object is found by adding the `draft` endpoint.

## Introduction
A record can exist in several states. Immediately after creation a record enters the 'draft' state. In this state the record is only accessible by its owner and can be freely modified: its metadata can be changed and files can be uploaded into or removed from it. A draft can be published at any time, and through this action it changes its state from 'draft' to 'published', is assigned Persistent Identifiers, and becomes publicly accessible. Please note that the list of files in a published record cannot be changed without versioning the record.

To update the metadata of a record through the API, a JSON Patch must be supplied with the request. Please read the documentation on this website carefully to fully understand how these patches work. In the request below, the term 'JSONPath' is used which indicates a path in the metadata relative to the root of the structure.

## Getting metadata schema information
Every record is published as part of a community. Each community has specific metadata schemas designed to cover the necessary information in order to easily understand and assess the contents of a publication. If an update needs to be made to the metadata fields and/or values, first the community's metadata schema needs to be examined to understand which fields can be added or updated.

Create a payload containig your token for authentication:

```python
>>> params = {'access_token': token}
```

Lets determine the draft record's community identifier as stored in its metadata:

```python
>>> recordid = 'b43a0e6914e34de8bd19613bcdc0d364'
>>> url = "https://trng-b2share.eudat.eu/api/records/" + recordid + "/draft"
>>> r = requests.get(url, params=params)
>>> result = json.loads(r.text)
>>> print(result["metadata"]["community"])
e9b9792e-79fb-4b07-b6b4-b9c2bd06d095
```

With this community identifier, the community metadata schema can be retrieved and required metadata fields listed. Refer to the [Get community metadata schema](03_Communities.md#get-community-metadata-schema) section of the [Communities](03_Communities.md) guide to see how to achieve this.

## Updating metadata
To update a draft record's metadata, the record identifier is required while making patch requests. The procedure can be applied to either draft or published records.

#### Preparing your new metadata
An object with the new and updated metadata fields and values needs to be constructed. As the community, title and open access check have already been set when the draft record was created, only some missing fields are provided:

```python
>>> metadata = {"creators": "B2SHARE-Training author",
                "description": "My first dataset ingested using the B2SHARE API",
                "licence": "CC-0-BY",
                "contact_email": "email@example.com"}
```

To update community-specific metadata fields, some additional information needs to be provided. Furthermore, to add or remove an item of a list of value, the JSON Patch requires specific paths. See the section [Administering community-specific fields](#administering-community-specific-fields).

#### Creating a JSON patch
The metadata update call is made using a patch request containing the patch operations and headers. Note that:

- The `api/records/<record_id>/draft` API end-point is used since our record is not yet published
- The metadata updates for the record must be provided in the [JSON patch format](http://jsonpatch.com) in order to avoid to have to send all the existing metadata as well
- The patch format contains one or more JSONPath strings. The root of these paths is the metadata object, as this is the only mutable object

In order to successfully update the metadata, a JSON patch is created using the `jsonpatch` Python package. First, the original existing metadata of the record is retrieved which will later be altered:

```python
>>> url = "https://trng-b2share.eudat.eu/api/records/" + recordid + "/draft"
>>> r = requests.get(url, params=params)
>>> result = json.loads(r.text)
>>> metadata_old = result["metadata"]
>>> print(json.dumps(metadata_old, indent=4))
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
>>> print(patch)
[{"path": "/community_specific", "op": "remove"}, {"path": "/publication_state", "op": "remove"}, {"path": "/owners", "op": "remove"}, {"path": "/open_access", "op": "remove"}, {"path": "/community", "op": "remove"}, {"path": "/titles", "op": "remove"}, {"path": "/$schema", "op": "remove"}, {"path": "/publisher", "value": "EUDAT", "op": "add"}, {"path": "/contact_email", "value": "email@example.com", "op": "add"}, {"path": "/descriptions", "value": [{"description": "My first dataset ingested using the B2SHARE API", "description_type": "Abstract"}], "op": "add"}, {"path": "/language", "value": "en_GB", "op": "add"}]
```

The current patch will remove any existing fields not present in the new metadata object, therefore these need to be removed in the final patch:

```python
>>> finpatch = filter(lambda x: x["op"] != "remove", patch)
>>> print(list(finpatch))
[{u'path': u'/publisher', u'value': 'EUDAT', u'op': u'add'}, {u'path': u'/contact_email', u'value': 'email@example.com', u'op': u'add'}, {u'path': u'/descriptions', u'value': [{'description': 'My first dataset ingested using the B2SHARE API', 'description_type': 'Abstract'}], u'op': u'add'}, {u'path': u'/language', u'value': 'en_GB', u'op': u'add'}]
```

The patch needs to be provided to the `data` argument as a serialized string for which the JSON package can be used:

```python
>>> strpatch = json.dumps(list(finpatch))
>>> print(strpatch)
[{"path": "/publisher", "value": "EUDAT", "op": "add"}, {"path": "/contact_email", "value": "email@example.com", "op": "add"}, {"path": "/descriptions", "value": [{"description": "My first dataset ingested using the B2SHARE API", "description_type": "Abstract"}], "op": "add"}, {"path": "/language", "value": "en_GB", "op": "add"}]
```

This section does not address the altering of community-specific metadata fields and multivalue fields. See the [Advanced metadata updates](#advanced-metadata-updates) section for more information.

#### Submitting the patch
The serialized JSON patch is sent to the service in order to update the metadata.

First, the request headers need to be defined:

```python
>>> header = {'Content-Type': 'application/json-patch+json'}
```

Now, the request response text shows the updated metadata:

```python
>>> url = 'https://trng-b2share.eudat.eu/api/records/' + recordid + "/draft"
>>> r = requests.patch(url, data=strpatch, params=params, headers=header)
>>> print(r)
<Response [200]>
>>> result = json.loads(r.text)
>>> print(json.dumps(result, indent=4))
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
>>> print(result["created"], result["updated"])
2017-03-02T16:34:26.383505+00:00 2017-03-02T17:03:37.500387+00:00
```

In case the patch request did not succeed (status code 400), an error description containing all errors is returned in the request response text. For example, the `creators` field value needs to be an array:

```python
>>> patch = '[{"path": "/creators", "value": "B2SHARE-Training author", "op": "add"}]'
>>> r = requests.patch(url, data=patch, params=params, headers=header)
>>> print(r.status_code)
400
>>> print(r.text)
{"message": "Validation error.", "status": 400, "errors": [{"message": "'B2SHARE-Training author' is not of type 'array'", "field": "creators"}]}
```

See the next section how to handle multivalue metadata fields.

## Advanced metadata updates
In the previous section, the default metadata fields of a record were updated using simple examples. In case the values of a multivalue metadata field must be managed, and likewise for the fields of a community-specific metadata schema, some additional steps need to be taken.

### Updating community-specific fields
Most communities have community-specific fields defined in a separate metadata schema. The values for these fields of a given record can be found in the metadata response when requesting it through the API.

In order to add, change or remove the value(s) of a community-specific metadata field, the specific metadata schema identifier used by the community is required. This identifier can be found by checking out the (draft) record's metadata values for community-specific fields of the _specific version_ of the community metadata schema used by that record. Unfortunately, currently it is a little cumbersome to find the right schema identifier, but it is possible.

To determine the identifier of this specific schema version, find the URL of the metadata schema used in the record's metadata:

```python
>>> recordid = '9e2f1bfa34ca402c96ff37b201b1a3aa'
>>> url = 'https://trng-b2share.eudat.eu/api/records/' + recordid + "/draft"
>>> r = requests.get(url, params=params)
>>> print(r.json()['metadata']['$schema'])
https://trng-b2share.eudat.eu/api/communities/0c97d6d2-88da-473a-8d30-2f4e730ed4a2/schemas/0#/draft_json_schema
```

Using this URL, the version identifier can be found by retrieving the schema and using the right metadata path:

```python
>>> s = requests.get(r.json()['metadata']['$schema'])
>>> schemaid = s.json()['json_schema']['allOf'][1]['properties']['community_specific']['required'][0]
>>> print(schemaid)
d562bab2-54b8-46f9-9ba8-f6e7f77ef5c5
```

To find out which fields are part of the community-specific fields of a metadata schema, locate the URL provided in the `community_specific` structure with the newly found schema identifier:

```python
>>> furl = s.json()['json_schema']['allOf'][1]['properties']['community_specific']['properties'][schemaid]['$ref']
>>> print(furl)
https://trng-b2share.eudat.eu/api/schemas/d562bab2-54b8-46f9-9ba8-f6e7f77ef5c5/versions/0#/json_schema
```

Again, using this URL, the community-specific field names can be found:

```python
>>> ff = requests.get(furl)
>>> print(ff.json()['json_schema']['properties'].keys())
dict_keys(['lat_max', 'lat_min', 'lon_max', 'lon_min', 'start_time', 'stop_time'])
```

To initialise the metadata field named `lat_max`, first examine the required structure for the field:

```python
>>> print(ff.json()['json_schema']['properties']['lat_max'])
{'description': 'Maximum latitude of the dataset', 'title': 'Latitude Max', 'type': 'string'}
```

Latitudes can be formatted in many ways. In this metadata schema the specific format is not specified and is therefore left to the reader to choose a format.

Now to set the value for this field, one of two possible patches must be used depending on whether any of the community-specific fields have already been set before in the record. If none of these fields are present in the current metadata of the record, use a patch in the first following section. If already one or more fields are set for the community-specific metadata schema, use the patch in the section thereafter.

##### Without existing community-specific fields
In this case, the container structure 'community_specific' does not exist yet and therefore it needs to be created with the patch. A string is expected, so use the following JSON Patch:

```python
>>> patch = [{"path": "/community_specific", "value": {schemaid: {"lat_max": "41 24.2028"}}, "op": "add"}]
>>> print(patch)
[{'path': '/community_specific', 'value': {'d562bab2-54b8-46f9-9ba8-f6e7f77ef5c5': {'lat_max': '41 24.2028'}}, 'op': 'add'}]
```

##### With existing community-specific fields
A string is expected, so use the following JSON Patch:

```python
>>> patch = [{"path": "/community_specific/" + schemaid + "/lat_max", "value": "41 24.2028", "op": "add"}]
>>> print(patch)
[{'path': '/community_specific/d562bab2-54b8-46f9-9ba8-f6e7f77ef5c5/lat_max', 'value': '41 24.2028', 'op': 'add'}]
```

Both of these patches will set the string '41 24.2028' as the value for the community-specific field `lat_max`. If the value has already been set, you must use 'replace' as the value for the operation in the `op` subfield of the patch.

##### Submitting the patch
See the [Submitting the patch](#submitting-the-patch) section how to submit this patch.

### Updating multivalue fields
Metadata fields can be defined to be 'multivalue' fields meaning that this field can have multiple values of the same type. For example, the `titles` field is defined to be an array of objects, where each object contains a `title` and a `title_type` field.

To change the current title(s) of a given (draft) record to a different single value, use the following patch:

```python
>>> patch = [{"path": "/titles", "value": [{"title": "Some title"}], "op": "replace"}]
```

In this case, if the operator is changed to 'add', all titles will still be replaced. To add a new title to the current set of titles, an index needs to be added to the `path` so the new value is added before that index. To add a new title as the first title omit the use of an array and use the operator 'add', as in the following patch:

```python
>>> patch = [{"path": "/titles/0", "value": {"title": "Some title first"}, "op": "add"}]
```

Now to replace the second title, use the following patch, again not using an array and using the 'replace' operator:

```python
>>> patch = [{"path": "/titles/1", "value": {"title": "Some title last"}, "op": "replace"}]
```

To immediately set three different titles, use the patch below. Note that the items in the array need to be unique, otherwise it will not be accepted by B2SHARE:

```python
>>> patch = [{"path": "/titles", "value": [{"title": "Some title first"}, {"title": "Some title second"}, {"title": "Some title other"}], "op": "add"}]
```

For a complete overview on JSON Patch operations and structure, see the [official documentation](http://jsonpatch.com/#operations).

## Updating all community metadata fields
If you are publishing datasets as part of specific communities, often all metadata fields that the community specifies in the community metadata schema need to be provided upon commit. For a strategy to achieve this, please follow the next [Update all community metadata fields](07_Update_all_community_metadata_fields.md) guide.
