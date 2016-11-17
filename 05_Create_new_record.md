# Create a new record
When your dataset is ready for publication, it can be uploaded to the B2SHARE service by creating a draft record and adding files and metadata. This page will guide you through the creation process of a new draft record and publishing it as a record. It covers:

 - the creation of a new draft record,
 - the addition of files and metadata and
 - the final completion.

Please note that the B2SHARE service makes a distinction between the two terms `record` and `draft record` (or simply `draft`). A **record** is unchangeable and has a persistent identifier (PID) assigned to it. A user can create a record by **first creating a draft record**, which is modifiable. Files and metadata can be placed into a draft record, but not into a record.

### Setup your connection
Please make sure your machine has been properly set up to use Python and required packages. Follow [this](A_Setup_and_install.md) guide in order to do so.

This guide assumes you have successfully registered your account on the [B2SHARE website](https://trng-b2share.eudat.eu) using your institutional credentials or social ID through B2ACCESS. In addition, the loading of the token, importing Python packages and checking request responses will not be covered here.

### Deposit workflow
In the following diagram the general deposit workflow of B2SHARE is shown. All blue boxes require a request interaction with the B2SHARE service.

![B2SHARE deposit workflow](img/B2SHARE-deposit-workflow.png "B2SHARE deposit workflow")

The red boxes indicate an object state, where in this workflow only drafts and records exist. Metadata (yellow) has to be manually added in the commit request. Persistent identifiers (PIDs) and checksum are automatically added by B2SHARE (green boxes).

### Create a new draft record
After loading your token a post request will create a new draft record. Only some basic metadata is needed, like the title and community, which is sent along with the request as the data argument together with a header defining the content type. All metadata can be changed later during the deposit workflow.

In this case, a new open access record is created for the EUDAT community with the title 'My test upload':

```python
>>> header = {"Content-Type": 'application/json'}
>>> metadata = {"title": "My test upload",
                "community": "e9b9792e-79fb-4b07-b6b4-b9c2bd06d095",
                "open_access": True}
>>> r = requests.post('https://vm0045.kaj.pouta.csc.fi/api/records', params={'access_token': token}, data=metadata, headers=header, verify=False)
```

On success, the response status code and text will be different this time:

```python
>>> print r
<Response [201]>
>>> result = json.loads(r.text)
>>> print json.dumps(result, indent=4)
{
    "updated": "2016-11-17T13:14:42.155426+00:00",
    "metadata": {
        "publication_state": "draft",
        "owners": [
            111
        ],
        "title": "My test upload",
        "open_access": true,
        "community": "e9b9792e-79fb-4b07-b6b4-b9c2bd06d095",
        "$schema": "https://vm0045.kaj.pouta.csc.fi/api/communities/e9b9792e-79fb-4b07-b6b4-b9c2bd06d095/schemas/0#/draft_json_schema"
    },
    "id": "fe5937afaad34d5e929053c9f66a7aca",
    "links": {
        "files": "https://vm0045.kaj.pouta.csc.fi/api/files/5b54daea-1219-4406-8899-abc722aee57b",
        "self": "https://vm0045.kaj.pouta.csc.fi/api/records/fe5937afaad34d5e929053c9f66a7aca/draft",
        "publication": "https://vm0045.kaj.pouta.csc.fi/api/records/fe5937afaad34d5e929053c9f66a7aca"
    },
    "created": "2016-11-17T13:14:42.155419+00:00"
}
```

Response code 201 indicates the draft record has been successfully created. The record ID `id` in the response text is used to identify the draft record during the additional steps of adding files and metadata:

```python
>>> result = json.loads(r.text)
>>> draftid = result["id"]
>>> print draftid
fe5937afaad34d5e929053c9f66a7aca
```

The record is still in a draft state, as is indicated in the `publication_state` property:

```python
>>> print result["publication_state"]
draft
```

After creation, the next steps are to add files and metadata. This can be done in any order and repeatedly after each addition. In the next sections, both procedures are explained.

### Add files to your new draft record
After creation of the draft record, files can be added. This is achieved in a similar way as the previous example via a POST request. Make sure your data files are accessible in the Python session. In this case the files named `sequence.txt` and `sequence2.txt` are added to the draft record.

Files in records are placed in file buckets attached to a record with a specific `file_bucket_id`. This identifier can be extraced from the returned information after creating the draft record in the nested property `files` of the property `links`:

```python
>>> filebucketid = result["links"]["files"].split('/')[-1]
>>> print filebucketid
5b54daea-1219-4406-8899-abc722aee57b
```

First, define a dictionary which contains Python open calls to the files. Files are added one-by-one:

```python
>>> files = {'file': open('sequence.txt', 'rb')}
```

In this statement, the action of opening the file is not actually performed. The file will be read only when the request is done.

Define the request URL by adding the file bucket ID and `files` end point:

```python
>>> url = 'https://trng-b2share.eudat.eu/api/files/' + filebucketid
>>> payload = {'access_token': token}
```

The complete request looks as follows:

```python
>>> r = requests.post(url + '/sequence.txt', files=files, params=payload, verify=False)
```

If the request is successful, the result can be checked:

```python
>>> print r.status_code
200
>>> result = json.loads(r.text)
>>> print json.dumps(result, indent=4)
{
    "mimetype": "text/plain",
    "updated": "2016-11-17T13:47:53.778257+00:00",
    "links": {
        "self": "https://vm0045.kaj.pouta.csc.fi/api/files/5b54daea-1219-4406-8899-abc722aee57b/sequence.txt",
        "version": "https://vm0045.kaj.pouta.csc.fi/api/files/5b54daea-1219-4406-8899-abc722aee57b/sequence.txt?versionId=1af9bf17-38b4-4857-afd4-a1a5afb2f537",
        "uploads": "https://vm0045.kaj.pouta.csc.fi/api/files/5b54daea-1219-4406-8899-abc722aee57b/sequence.txt?uploads"
    },
    "is_head": true,
    "created": "2016-11-17T13:47:53.772521+00:00",
    "checksum": "md5:7485383a6d14f45aa8ad265ef80f0e15",
    "version_id": "1af9bf17-38b4-4857-afd4-a1a5afb2f537",
    "delete_marker": false,
    "key": "sequence.txt",
    "size": 1091
}
```

The mime-type is detected, direct links are given and a checksum is calculated.

If the request fails, check the error by displaying the response text, for example when the `files` object has errors:

```python
>>> print r
<Response [404]>
```

The reponse text will, in this case, a HTML page describing the error.

When the upload file is not accessible:
```python
>>> print r.status_code
400
>>> result = json.loads(r.text)
>>> print json.dumps(result, indent=4)
{
    "status": 400,
    "message": "The browser (or proxy) sent a request that this server could not understand."
}
```

Repeat the above steps to add other files.

#### Check your uploaded files

When all your files have been uploaded, you can check the draft record's current status regarding these files using the URL with a GET request:

```python
>>> r = requests.get(url, params=payload, verify=False)
>>> result = json.loads(r.text)
>>> print json.dumps(result, indent=4)
{
    "max_file_size": 1048576000,
    "updated": "2016-11-17T15:11:57.545493+00:00",
    "locked": false,
    "links": {
        "self": "https://vm0045.kaj.pouta.csc.fi/api/files/5b54daea-1219-4406-8899-abc722aee57b",
        "uploads": "https://vm0045.kaj.pouta.csc.fi/api/files/5b54daea-1219-4406-8899-abc722aee57b?uploads",
        "versions": "https://vm0045.kaj.pouta.csc.fi/api/files/5b54daea-1219-4406-8899-abc722aee57b?versions"
    },
    "created": "2016-11-17T13:14:42.219788+00:00",
    "quota_size": null,
    "id": "5b54daea-1219-4406-8899-abc722aee57b",
    "contents": [
        {
            "mimetype": "text/plain",
            "updated": "2016-11-17T13:47:53.778257+00:00",
            "links": {
                "self": "https://vm0045.kaj.pouta.csc.fi/api/files/5b54daea-1219-4406-8899-abc722aee57b/sequence.txt",
                "version": "https://vm0045.kaj.pouta.csc.fi/api/files/5b54daea-1219-4406-8899-abc722aee57b/sequence.txt?versionId=1af9bf17-38b4-4857-afd4-a1a5afb2f537",
                "uploads": "https://vm0045.kaj.pouta.csc.fi/api/files/5b54daea-1219-4406-8899-abc722aee57b/sequence.txt?uploads"
            },
            "is_head": true,
            "created": "2016-11-17T13:47:53.772521+00:00",
            "checksum": "md5:7485383a6d14f45aa8ad265ef80f0e15",
            "version_id": "1af9bf17-38b4-4857-afd4-a1a5afb2f537",
            "delete_marker": false,
            "key": "sequence.txt",
            "size": 1091
        },
        {
            "mimetype": "text/plain",
            "updated": "2016-11-17T15:11:57.521926+00:00",
            "links": {
                "self": "https://vm0045.kaj.pouta.csc.fi/api/files/5b54daea-1219-4406-8899-abc722aee57b/sequence2.txt",
                "version": "https://vm0045.kaj.pouta.csc.fi/api/files/5b54daea-1219-4406-8899-abc722aee57b/sequence2.txt?versionId=b37d9332-e84e-4e83-b160-c7bcd68d847c",
                "uploads": "https://vm0045.kaj.pouta.csc.fi/api/files/5b54daea-1219-4406-8899-abc722aee57b/sequence2.txt?uploads"
            },
            "is_head": true,
            "created": "2016-11-17T15:11:57.515704+00:00",
            "checksum": "md5:9320ae4acf92fe5d4ddbac836cd3d745",
            "version_id": "b37d9332-e84e-4e83-b160-c7bcd68d847c",
            "delete_marker": false,
            "key": "sequence2.txt",
            "size": 11892
        }
    ],
    "size": 12983
}
```

A list of two files is returned, including the files' sizes. You can do this with every file bucket, as long as you have the file bucket ID.

### Add new metadata to your draft record
Metadata is added to a draft record by issuing a HTTP patch request with a JSON patch list of operations that add or update metadata fields with corresponding values. Some of the fields are required by the metadata schema, other are optional. Refer to [Request and Metadata Reference Guide](B_Request_and_Metadata_Reference_Guide.md) to get the required and optional list of fields used for metadata.

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
>>> url = "https://vm0045.kaj.pouta.csc.fi/api/records/fe5937afaad34d5e929053c9f66a7aca/draft"
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
>>> url = "https://vm0045.kaj.pouta.csc.fi/api/records/fe5937afaad34d5e929053c9f66a7aca/draft"
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

### Commit the changes
The final step will complete the draft record by altering it using a patch request. After this request, the files of the record are immutable!

In this case, the only thing that needs to be changed is the patch string. As only the `publication_state` metadata field will be set to 'published', the patch is created directly as a string without using the `jsonpatch` package:
```python
>>> commit = '[{"op": "add", "path":"/publication_state", "value": "published"}]'
```

The final commit request will return the updated object metadata in case the request is successfull (status code 200):
```python
>>> r = requests.patch(url, data=commit, params={'access_token': token}, headers=header, verify=False)
>>> print r.status_code
200
>>> result = json.loads(r.text)
>>> print json.dumps(result, indent=4)
{
    "updated": "2016-11-17T16:44:58.353793+00:00",
    "metadata": {
        "publication_state": "published",
        "open_access": true,
        "DOI": "10.5072/b2share.2c6f2947-450d-4b62-b557-a83d41482988",
        "description": "My first dataset ingested using the B2SHARE API",
        "title": "My test upload",
        "ePIC_PID": "http://hdl.handle.net/11304/4bdfbc58-bb3e-400c-b4df-38053e7a014e",
        "community": "e9b9792e-79fb-4b07-b6b4-b9c2bd06d095",
        "contact_email": "email@example.com",
        "licence": "CC-0-BY",
        "owners": [
            111
        ],
        "$schema": "https://vm0045.kaj.pouta.csc.fi/api/communities/e9b9792e-79fb-4b07-b6b4-b9c2bd06d095/schemas/0#/draft_json_schema",
        "creators": [
            "B2SHARE-Training author"
        ]
    },
    "id": "fe5937afaad34d5e929053c9f66a7aca",
    "links": {
        "files": "https://vm0045.kaj.pouta.csc.fi/api/files/5b54daea-1219-4406-8899-abc722aee57b",
        "self": "https://vm0045.kaj.pouta.csc.fi/api/records/fe5937afaad34d5e929053c9f66a7aca/draft",
        "publication": "https://vm0045.kaj.pouta.csc.fi/api/records/fe5937afaad34d5e929053c9f66a7aca"
    },
    "created": "2016-11-17T13:14:42.155419+00:00"
}
```

An EPIC persistent identifier and DOI (`ePIC_PID` and `DOI` fields) have been automatically generated and added to the metadata. The `owners` field array contains the internal user IDs.

### Check and display your results
Once the deposit process is completed, the results can be checked by requesting the record data using the new record ID. Follow the [record retrieval guide](01_Retrieve_existing_record.md) for an extensive description on how to do this.

The record ID `id` in the response message can directly be used to see the landing page of the newly created deposit: [fe5937afaad34d5e929053c9f66a7aca](https://vm0045.kaj.pouta.csc.fi/records/fe5937afaad34d5e929053c9f66a7aca). If the page displays a restriction message, this is due the server-side processing of the ingestion. As soon as this is finished, the message will disappear.

Unfortunately, some of the metadata schema fields are missing since during the metadata update step, these fields were not added to the patch. It is highly recommended to complete all fields during this step in order to increase the discoverability, authenticity and reusability of the dataset.
