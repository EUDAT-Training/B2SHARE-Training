# Update record metadata
In some cases the metadata fields and values of draft or published records need to be changed in order to correct small mistakes or add missing metadata fields. In this guide the editing of metadata of both published and draft records is explained.

Please note that altering the metadata of a published record will generate a new version of that record with new PIDs and checksums. The original version of the record will always be discoverable and citeable, unless it is taken offline.

This guide covers:

- Preparing new metadata
- Creating a JSON patch
- Submitting your patch
- Inspecting the result

Refer to [Request and Metadata Reference Guide](B_Request_and_Metadata_Reference_Guide.md) to get the required and optional list of fields used for metadata.

## Updating metadata
In order to update a record's metadata, the record ID is required while making patch requests. The procedure can be applied to either draft or published records.

First, the request headers need to be defined:
```python
>>> header = {'Content-Type': 'application/json-patch+json'}
```

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

In order to successfully update the metadata, a JSON patch is created using the `jsonpatch` Python package. First, the original existing metadata of the record is retrieved:
```python
>>> url = "https://vm0045.kaj.pouta.csc.fi/api/records/' + recordid + '/draft"
>>> r = requests.get(url, params=payload, verify=False)
>>> result = json.loads(r.text)
>>> metadata_old = result["metadata"]
>>> print json.dumps(metadata_old, indent=4)
{
    "publication_state": "draft",
    "owners": [
        111
    ],
    "title": "My test upload",
    "open_access": true,
    "community": "e9b9792e-79fb-4b07-b6b4-b9c2bd06d095",
    "$schema": "https://vm0045.kaj.pouta.csc.fi/api/communities/e9b9792e-79fb-4b07-b6b4-b9c2bd06d095/schemas/0#/draft_json_schema"
}
```

The actual JSON patch is created by:
```python
>>> patch = jsonpatch.make_patch(metadata_old, metadata)
>>> print patch
[{"path": "/publication_state", "op": "remove"}, {"path": "/owners", "op": "remove"}, {"path": "/title", "op": "remove"}, {"path": "/open_access", "op": "remove"}, {"path": "/community", "op": "remove"}, {"path": "/$schema", "op": "remove"}, {"path": "/creators", "value": "B2SHARE-Training author", "op": "add"}, {"path": "/contact_email", "value": "email@example.com", "op": "add"}, {"path": "/description", "value": "My first dataset ingested using the B2SHARE API", "op": "add"}, {"path": "/licence", "value": "CC-0-BY", "op": "add"}]
```

The current patch will remove any existing fields not present in the metadata object, therefore these are removed in the final patch:
```python
>>> finpatch = [d for d in patch if d["op"] <> "remove"]
>>> print finpatch
[{u'path': u'/creators', u'value': 'B2SHARE-Training author', u'op': u'add'}, {u'path': u'/contact_email', u'value': 'email@example.com', u'op': u'add'}, {u'path': u'/description', u'value': 'My first dataset ingested using the B2SHARE API', u'op': u'add'}, {u'path': u'/licence', u'value': 'CC-0-BY', u'op': u'add'}]
```

The patch needs to be provided to the `data` argument as a serialized string and because Python by default adds a unicode indication to any string value, some additional processing is needed. Without any specific Python packages this can be done as follows:
```python
>>> strpatch = "[%s]" % ",".join([json.dumps(x) for x in finpatch])
>>> print strpatch
[{"path": "/creators", "value": ["B2SHARE-Training author"], "op": "add"},{"path": "/contact_email", "value": "email@example.com", "op": "add"},{"path": "/description", "value": "My first dataset ingested using the B2SHARE API", "op": "add"},{"path": "/licence", "value": "CC-0-BY", "op": "add"}]
```

#### Submitting the patch
The serialized JSON patch is sent to the service in order to update the metadata. First, the header of the request needs to be set:
```python
>>> header = {'Content-Type': 'application/json-patch+json'}
```

Now, the request response text shows the updated metadata:
```python
>>> url = "https://vm0045.kaj.pouta.csc.fi/api/records/' + recordid + '/draft"
>>> r = requests.patch(url, data=strpatch, params=payload, headers=header, verify=False)
>>> print r
<Response [200]>
>>> result = json.loads(r.text)
>>> print json.dumps(result, indent=4)
{
  "created": "2016-11-17T13:14:42.155419+00:00",
  "id": "fe5937afaad34d5e929053c9f66a7aca",
  "links": {
    "files": "https://vm0045.kaj.pouta.csc.fi/api/files/5b54daea-1219-4406-8899-abc722aee57b",
    "publication": "https://vm0045.kaj.pouta.csc.fi/api/records/fe5937afaad34d5e929053c9f66a7aca",
    "self": "https://vm0045.kaj.pouta.csc.fi/api/records/fe5937afaad34d5e929053c9f66a7aca/draft"
  },
  "metadata": {
    "$schema": "https://vm0045.kaj.pouta.csc.fi/api/communities/e9b9792e-79fb-4b07-b6b4-b9c2bd06d095/schemas/0#/draft_json_schema",
    "community": "e9b9792e-79fb-4b07-b6b4-b9c2bd06d095",
    "contact_email": "email@example.com",
    "creators": [
      "B2SHARE-Training author"
    ],
    "description": "My first dataset ingested using the B2SHARE API",
    "licence": "CC-0-BY",
    "open_access": true,
    "owners": [
      111
    ],
    "publication_state": "draft",
    "title": "My test upload"
  },
  "updated": "2016-11-17T16:32:35.601059+00:00"
}
```

Compare the created and updated metadata timestamp:
```python
>>> print result["created"], result["updated"]
2016-11-17T13:14:42.155419+00:00 2016-11-17T16:32:35.601059+00:00
```

In case the patch request did not succeed (status code 400), an error description containing all errors is returned in the request response text. For example, the `creators` field value needs to be an array:
```python
>>> patch = '[{"path": "/creators", "value": "B2SHARE-Training author", "op": "add"}]'
>>> r = requests.patch(url, data=patch, params=payload, headers=header, verify=False)
>>> print r.status_code
400
>>> print r.text
{"message": "Validation error.", "status": 400, "errors": [{"message": "'B2SHARE-Training author' is not of type 'array'", "field": "creators"}]}
```
