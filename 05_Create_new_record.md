# Create a new record
When your dataset is ready for publication, it can be uploaded to the B2SHARE service by creating a draft record and adding files and metadata. This page will guide you through the creation process of a new draft records, preparing and finally publishing it as a record. It covers:

 - The creation of a new draft record,
 - The addition of files and metadata and
 - Committing the draft record to publish it

Please note that the B2SHARE service makes a distinction between the two terms `record` and `draft record` (or simply `draft`). A **record** is published and therefore unchangeable and has persistent identifiers (PID) assigned to it, as well as checksums. A user can create a record by **first creating a draft record**, which is modifiable. Files and metadata can be placed into a draft record, but not into a record.

It is possible to create a new version of your record with new metadata and PIDs, the old version though will remain intact without alteration and is still identifiable and referable.

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

Response code 201 indicates the draft record has been successfully created. The record ID metadata field `id` in the response text is used to identify the draft record during the additional steps of adding files and metadata:

```python
>>> result = json.loads(r.text)
>>> recordid = result["id"]
>>> print recordid
fe5937afaad34d5e929053c9f66a7aca
```

The record is still in a draft state, as is indicated in the `publication_state` property:

```python
>>> print result["publication_state"]
draft
```

After creation, the next steps are to add files and metadata. This can be done in any order and repeatedly after each addition. In the next sections, both procedures are explained.

Please note that the record ID will remain the same during the draft stage and after finally publishing the record.

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
>>> url = 'https://vm0045.kaj.pouta.csc.fi/api/files/' + filebucketid
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

The mime-type is detected, direct links are given and a checksum is calculated. The `version_id` can be used to refer to this specific upload of the file in case new versions are uploaded later on.

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

### Add additional metadata to your draft record
Metadata is added to a draft record by issuing a HTTP patch request with a JSON patch list of operations that add or update metadata fields with corresponding values.

Since this procedure is quite extensive, refer to the [Update record metadata](06_Update_record_metadata.md) module to update your draft record's current metadata.

### Publishing your draft record
The final step will complete the draft record by altering it using a patch request. After this request, the files of the record are immutable and your record is published!

In this case, the only thing that needs to be changed is the value of the `publication_state` metadata field. The metadata field will be set to 'published', and therefore the patch can be created directly as a string without using the `jsonpatch` package:
```python
>>> commit = '[{"op": "add", "path":"/publication_state", "value": "published"}]'
```

The final commit request will return the updated object metadata in case the request is successfull (status code 200):
```python
>>> url = "https://vm0045.kaj.pouta.csc.fi/api/records/" + recordid + "/draft"
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

Your draft record is now published as a new record!

An EPIC persistent identifier and DOI (`ePIC_PID` and `DOI` fields) have been automatically generated and added to the metadata. The `owners` field array contains the internal user IDs.

A published record will always have a draft record equivalent. If you ever want to change any of the records metadata, then the draft record can be immediately used for this process.

### Check and display your results
Once the deposit process is completed, the results can be checked by requesting the record data using the new record ID. Follow the [record retrieval guide](01_Retrieve_existing_record.md) for an extensive description on how to do this.

The record ID `id` in the response message can directly be used to see the landing page of the newly created deposit: [fe5937afaad34d5e929053c9f66a7aca](https://vm0045.kaj.pouta.csc.fi/records/fe5937afaad34d5e929053c9f66a7aca). If the page displays a restriction message, this is due the server-side processing of the ingestion. As soon as this is finished, the message will disappear.

Unfortunately, some of the metadata schema fields are missing since during the metadata update step, these fields were not added to the patch. It is highly recommended to complete all fields during this step in order to increase the discoverability, authenticity and reusability of the dataset.
