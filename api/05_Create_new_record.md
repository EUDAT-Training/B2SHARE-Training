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

The red boxes indicate an object state, where in this workflow only drafts and records exist. Files and metadata can be added multiple times. Persistent identifiers (PIDs) and checksum are automatically added by B2SHARE (green boxes).

### Create a new draft record
After loading your token a post request will create a new draft record. Only some basic metadata is needed, like the title and community, which is sent along with the request as the data argument together with a header defining the content type. All metadata can be changed later during the deposit workflow.

In this case, a new open access record is created for the EUDAT community with the title 'My test upload':

```python
>>> header = {"Content-Type": 'application/json'}
>>> metadata = {"titles":[{"title":"My test upload"}],
                "community": "e9b9792e-79fb-4b07-b6b4-b9c2bd06d095",
                "open_access": True}
>>> r = requests.post('https://trng-b2share.eudat.eu/api/records/', params={'access_token': token},
                data=metadata, headers=header, verify=False)
```

Please note the trailing slash (`/`) at the end of the URL. Without it, the request will currently not work.

On success, the response status code and text will be different this time:

```python
>>> print r
<Response [201]>
>>> result = json.loads(r.text)
>>> print json.dumps(result, indent=4)
{
    "updated": "2017-02-03T09:24:57.838332+00:00",
    "metadata": {
        "community_specific": {},
        "publication_state": "draft",
        "owners": [
            12
        ],
        "open_access": true,
        "community": "e9b9792e-79fb-4b07-b6b4-b9c2bd06d095",
        "titles": [
            {
                "title": "My test upload"
            }
        ],
        "$schema": "https://trng-b2share.eudat.eu/api/communities/e9b9792e-79fb-4b07-b6b4-b9c2bd06d095/schemas/0#/draft_json_schema"
    },
    "id": "2a441018bf254cd28ba336613186e6f2",
    "links": {
        "files": "https://trng-b2share.eudat.eu/api/files/bbb85e9f-1640-4299-a7c8-b0a4b29df4cf",
        "self": "https://trng-b2share.eudat.eu/api/records/2a441018bf254cd28ba336613186e6f2/draft",
        "publication": "https://trng-b2share.eudat.eu/api/records/2a441018bf254cd28ba336613186e6f2"
    },
    "created": "2017-02-03T09:24:57.838323+00:00"
}
```

Response code 201 indicates the draft record has been successfully created. The record ID metadata field `id` in the response text is used to identify the draft record during the additional steps of adding files and metadata:

```python
>>> result = json.loads(r.text)
>>> recordid = result["id"]
>>> print recordid
2a441018bf254cd28ba336613186e6f2
```

The record is still in a draft state, as is indicated in the `publication_state` property:

```python
>>> print result["publication_state"]
draft
```

After creation, the next steps are to add files and metadata. This can be done in any order and repeatedly after each addition. In the next sections, both procedures are explained.

Please note that the record ID will remain the same during the draft stage and after finally publishing the record.

### Add files to your new draft record
After creation of the draft record, files can be added. This is achieved in a similar way as the previous example via a PUT request. Make sure your data files are accessible in the Python session. In this case the files named `sequence.txt` and `sequence2.txt` are added to the draft record.

Files in records are placed in file buckets attached to a record with a specific `file_bucket_id`. This identifier can be extraced from the returned information after creating the draft record in the nested property `files` of the property `links`:

```python
>>> filebucketid = result["links"]["files"].split('/')[-1]
>>> print filebucketid
bbb85e9f-1640-4299-a7c8-b0a4b29df4cf
```

First, define a dictionary which contains Python open calls to the files. Files are added one-by-one:

```python
>>> upload_file = open('sequence.txt', 'rb')
```

In this statement, the action of reading the file is not actually performed. The file will be read only when the request is done and send as a direct stream.

Define the request URL by adding the file bucket ID to the `files` end point and define the request header:

```python
>>> url = 'https://trng-b2share.eudat.eu/api/files/' + filebucketid
>>> payload = {'access_token': token}
>>> header = {"Accept": "application/json", "Content-Type": "application/octet-stream"}
```

The complete put request looks as follows:

```python
>>> r = requests.put(url + '/sequence.txt', files=upload_file, params=payload, headers=header, verify=False)
```

If the request is successful, the result can be checked:

```python
>>> print r.status_code
200
>>> result = json.loads(r.text)
>>> print json.dumps(result, indent=4)
{
    "mimetype": "text/plain",
    "updated": "2017-02-03T09:55:33.654440+00:00",
    "is_head": true,
    "links": {
        "self": "https://trng-b2share.eudat.eu/api/files/bbb85e9f-1640-4299-a7c8-b0a4b29df4cf/sequence2.txt",
        "version": "https://trng-b2share.eudat.eu/api/files/bbb85e9f-1640-4299-a7c8-b0a4b29df4cf/sequence2.txt?versionId=4d5efca2-cdb0-44d2-acef-4b679e670198",
        "uploads": "https://trng-b2share.eudat.eu/api/files/bbb85e9f-1640-4299-a7c8-b0a4b29df4cf/sequence2.txt?uploads"
    },
    "created": "2017-02-03T09:55:33.651024+00:00",
    "checksum": "md5:ef897a013eea4f7efef58bcac0251ada",
    "version_id": "4d5efca2-cdb0-44d2-acef-4b679e670198",
    "delete_marker": false,
    "key": "sequence2.txt",
    "size": 38
}
```

The mime-type is detected, direct links are given and a checksum is calculated. The `version_id` can be used to refer to this specific upload of the file in case new versions are uploaded later on.

If the request fails, check the error by displaying the response text, for example when the `files` object has errors. The reponse text will, in this case, a HTML page describing the error.

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
>>> r = requests.get('https://trng-b2share.eudat.eu/api/files/' + filebucketid, params=payload, verify=False)
>>> result = json.loads(r.text)
>>> print json.dumps(result, indent=4)
{
    "max_file_size": 1048576000,
    "updated": "2017-02-03T09:55:33.659236+00:00",
    "locked": false,
    "links": {
        "self": "https://trng-b2share.eudat.eu/api/files/bbb85e9f-1640-4299-a7c8-b0a4b29df4cf",
        "uploads": "https://trng-b2share.eudat.eu/api/files/bbb85e9f-1640-4299-a7c8-b0a4b29df4cf?uploads",
        "versions": "https://trng-b2share.eudat.eu/api/files/bbb85e9f-1640-4299-a7c8-b0a4b29df4cf?versions"
    },
    "created": "2017-02-03T09:24:57.857752+00:00",
    "quota_size": null,
    "id": "bbb85e9f-1640-4299-a7c8-b0a4b29df4cf",
    "contents": [
        {
            "mimetype": "text/plain",
            "updated": "2017-02-03T09:45:11.058574+00:00",
            "is_head": true,
            "links": {
                "self": "https://trng-b2share.eudat.eu/api/files/bbb85e9f-1640-4299-a7c8-b0a4b29df4cf/sequence.txt",
                "version": "https://trng-b2share.eudat.eu/api/files/bbb85e9f-1640-4299-a7c8-b0a4b29df4cf/sequence.txt?versionId=abfc82a0-c3a2-4f93-85da-07575df9ff86",
                "uploads": "https://trng-b2share.eudat.eu/api/files/bbb85e9f-1640-4299-a7c8-b0a4b29df4cf/sequence.txt?uploads"
            },
            "created": "2017-02-03T09:45:11.054631+00:00",
            "checksum": "md5:ef69caaaeea9c17120821a9eb6c7f1de",
            "version_id": "abfc82a0-c3a2-4f93-85da-07575df9ff86",
            "delete_marker": false,
            "key": "sequence.txt",
            "size": 192
        },
        {
            "mimetype": "text/plain",
            "updated": "2017-02-03T09:55:33.654440+00:00",
            "is_head": true,
            "links": {
                "self": "https://trng-b2share.eudat.eu/api/files/bbb85e9f-1640-4299-a7c8-b0a4b29df4cf/sequence2.txt",
                "version": "https://trng-b2share.eudat.eu/api/files/bbb85e9f-1640-4299-a7c8-b0a4b29df4cf/sequence2.txt?versionId=4d5efca2-cdb0-44d2-acef-4b679e670198",
                "uploads": "https://trng-b2share.eudat.eu/api/files/bbb85e9f-1640-4299-a7c8-b0a4b29df4cf/sequence2.txt?uploads"
            },
            "created": "2017-02-03T09:55:33.651024+00:00",
            "checksum": "md5:ef897a013eea4f7efef58bcac0251ada",
            "version_id": "4d5efca2-cdb0-44d2-acef-4b679e670198",
            "delete_marker": false,
            "key": "sequence2.txt",
            "size": 38
        }
    ],
    "size": 295
}
```

The links to the file bucket is displayed, as well as the 'contents' list of two files, including the files' sizes. You can do this with every file bucket, as long as you have the file bucket ID.

### Add additional metadata to your draft record
Metadata is added to a draft record by issuing a HTTP patch request with a JSON patch list of operations that add or update metadata fields with corresponding values.

Since this procedure is quite extensive, refer to the [Update record metadata](06_Update_record_metadata.md) module to update your draft record's current metadata. This module can also be used to update metadata of existing records.

### Publishing your draft record
The final step will complete the draft record by altering it using a patch request. After this request, the files of the record are immutable and your record is published!

In this case, the only thing that needs to be changed is the value of the `publication_state` metadata field. The metadata field will be set to 'submitted', and therefore the patch can be created directly as a string:
```python
>>> header = {'Content-Type': 'application/json-patch+json'}
>>> commit = '[{"op": "add", "path":"/publication_state", "value": "submitted"}]'
```

Also, the header of the request is set.

The final commit request will return the updated object metadata in case the request is successfull (status code 200):
```python
>>> url = "https://trng-b2share.eudat.eu/api/records/" + recordid + "/draft"
>>> r = requests.patch(url, data=commit, params={'access_token': token}, headers=header, verify=False)
>>> print r
<Response [200]>
>>> result = json.loads(r.text)
>>> print json.dumps(result, indent=4)
{
    "updated": "2017-02-03T10:16:54.744721+00:00",
    "metadata": {
        "community_specific": {},
        "publication_state": "published",
        "owners": [
            12
        ],
        "open_access": true,
        "community": "e9b9792e-79fb-4b07-b6b4-b9c2bd06d095",
        "titles": [
            {
                "title": "My test upload"
            }
        ],
        "$schema": "https://trng-b2share.eudat.eu/api/communities/e9b9792e-79fb-4b07-b6b4-b9c2bd06d095/schemas/0#/draft_json_schema"
    },
    "id": "2a441018bf254cd28ba336613186e6f2",
    "links": {
        "files": "https://trng-b2share.eudat.eu/api/files/bbb85e9f-1640-4299-a7c8-b0a4b29df4cf",
        "self": "https://trng-b2share.eudat.eu/api/records/2a441018bf254cd28ba336613186e6f2/draft",
        "publication": "https://trng-b2share.eudat.eu/api/records/2a441018bf254cd28ba336613186e6f2"
    },
    "created": "2017-02-03T09:24:57.838323+00:00"
}
```

Your draft record is now published as a new record and is available under the URL `https://trng-b2share.eudat.eu/api/records/2a441018bf254cd28ba336613186e6f2`!

An EPIC persistent identifier and DOI (`ePIC_PID` and `DOI` fields) have been automatically generated and added to the metadata. The `owners` field array contains the internal user IDs.

#### Important
A published record will always have a draft record equivalent. If you ever want to change any of the records metadata, then the draft record can be immediately used for this process.

Please note that the file bucket ID of the draft record differs from the file record ID of the published record. By retrieving the published record metadata, the new file bucket ID can be obtained from the corresponding URL:

```python
>>> r = requests.get('https://trng-b2share.eudat.eu/api/records/2a441018bf254cd28ba336613186e6f2', verify=False)
>>> result = json.loads(r.text)
>>> filebucket = result["links"]["files"]
>>> print filebucket
https://trng-b2share.eudat.eu/api/files/8421cc4a-8762-4708-b94b-ec04a3cf04ee
```

Using this URL the state of the file bucket of the published record can be investigated. It contains the exact same files as the draft version, but it is locked and therefore cannot be changed anymore:

```python
>>> r = requests.get(filebucket, verify=False)
>>> result = json.loads(r.text)
>>> print result["locked"]
True
```

### Check and display your results
Once the deposit process is completed, the results can be checked by requesting the record data using the new record ID. Follow the [record retrieval guide](01_Retrieve_existing_record.md) for an extensive description on how to do this.

The record ID `id` in the response message can directly be used to see the landing page of the newly created deposit: [2a441018bf254cd28ba336613186e6f2](https://trng-b2share.eudat.eu/records/2a441018bf254cd28ba336613186e6f2). If the page displays a restriction message, this is due the server-side processing of the ingestion. As soon as this is finished, the message will disappear.

Unfortunately, some of the metadata schema fields are missing since during the metadata update step, these fields were not added to the patch. It is highly recommended to complete all fields during this step in order to increase the discoverability, authenticity and reusability of the dataset. Please check the [Update record metadata](06_Update_record_metadata.md) module to update your published record's metadata.
