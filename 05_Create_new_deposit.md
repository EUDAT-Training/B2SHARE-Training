# Create a new deposit
When your dataset is ready for publication, it can be uploaded to the B2SHARE service by creating a deposition and adding files and metadata. This page will guide you through the creation process of a new deposition. It covers: 
 
 - the actual creation of a new record, 
 - the addition of files and metadata and 
 - the final completion.

Please note that the B2SHARE service makes a distinction between the two terms `record` and `deposition`. A **record** is unchangeable and has a persistent identifier (PID) assigned to it. A user can create a record by **first creating a deposition**, which is modifiable. Files and metadata can be placed into a deposition, but not into a record.

### Setup your connection
Please make sure your machine has been properly set up to use Python and required packages. Follow [this](A_Setup_and_install.md) guide in order to do so.

This guide assumes you have successfully registered your account on the [B2SHARE website](https://trng-b2share.eudat.eu) using your institutional credentials or social ID through B2ACCESS. In addition, the loading of the token, importing Python packages and checking request responses will not be covered here.

### Deposit workflow
In the following  diagram you may see the deposit workflow. All blue boxes require a request interaction with the B2SHARE service.

![B2SHARE deposition workflow](img/B2SHARE-deposition.png "B2SHARE deposition workflow")

The red boxes indicate an object state, where in this workflow only depositions and records can exist. Metadata (yellow) has to be manually added in the commit request. Persistent identifiers (PIDs) and checksums are automatically generated and added by the B2SHARE service (green boxes).

### Create a new deposit
After loading your token a simple post request will create a new deposition:

```python
r = requests.post('https://trng-b2share.eudat.eu/api/depositions', params={'access_token': token}, verify=False)
```

On success, the response code and text will be different this time:

```python
>>> print r
<Response [201]>
>>> print r.text
{"deposit_id": "4da53e5a210211e685780050569435ca", "message": "New deposition created", "location": "/api/deposition/4da53e5a210211e685780050569435ca"}
```

Response code 201 indicates the deposition has been successfully created. The deposition ID `deposit_id` in the response text is used to identify the deposition during the additional steps of adding files and metadata:

```python
>>> result = json.loads(r.text)
>>> depositid = result["deposit_id"]
>>> print depositid
4da53e5a210211e685780050569435ca
```

### Add files to your new deposit

After creation of the deposition, files need to be added. This is achieved in a similar way as the previous example via a POST request. Make sure your data files are accessible in the Python session. In this case the files named `sequence.txt` and `sequence2.txt` are added to the deposition.

First, define a dictionary which contains Python open calls to the files. Files are added one-by-one:

```python
>>> files = {'file': open('sequence.txt', 'rb')}
```

In this statement, the action of opening the file is not actually performed. The file will be read only when the request call is performed.

Define the request URL by adding the deposition ID and `files` end point:

```python
>>> url = 'https://trng-b2share.eudat.eu/api/deposition/' + depositid + '/files'
>>> payload = {'access_token': token}
```

The complete request looks as follows:

```python
>>> r = requests.post(url, files=files, params=payload, verify=False)
```

If the request is successful, the result can be checked:

```python
>>> print r
<Response [200]>
>>> print r.text
{"files": [{"name": "sequence.txt"}], "message": "File(s) saved"}
```

If the request fails, check the error by displaying the response text, for example when the deposition is not found:

```python
>>> print r
<Response [404]>
```

The reponse text will, in this case, a HTML page describing the error.

When the upload file is not accessible:
```python
>>> print r
<Response [400]>
>>> print r.text
{"files": [], "message": "No files", "errors": ["file sequence.txt is empty"]}
```

Repeat the above steps to add other files.

#### Check your uploaded files

When all your files have been uploaded, you can check the deposition's current status regarding these files using the same URL with a GET request:

```python
>>> r = requests.get(url, params=payload, verify=False)
>>> result = json.loads(r.text)
>>> print result["files"]
[{u'name': u'sequence.txt', u'size': 292}, {u'name': u'sequence2.txt', u'size': 3893}]
```

A list of two files are returned, including the files' sizes. You can do this with every deposition, as long as you have the deposition ID and it has not been committed.

### Commit the changes
The final step will complete the deposition by adding metadata and committing it. The metadata is included in the request as a list of key-value pairs. Some of the fields are required, other are optional. Refer to [Request and Metadata Reference Guide](B_Request_and_Metadata_Reference_Guide.md) to get the required and optional list of fields used for metadata.

First, an object containing the minimum required metadata fields plus the author field is constructed:
```python
>>> metadata = {"domain": "generic", "title": "My first dataset", "creator": ["B2SHARE-Training author"], 
...     "description": "My first dataset ingested using the API", "open_access": "true"}
```

In addition to the metadata, a header object is sent to set the return data type:
```python
>>> headers = {'content-type': 'application/json'}
```

The URL now needs to be postfixed by the `commit` end point:
```python
>>> url = 'https://trng-b2share.eudat.eu/api/deposition/' + depositid + '/commit'
```

The call is made using a POST request containing the metadata and headers. Please note that the metadata is serialized into a single string using the JSON package:
```python
>>> r = requests.post(url, data=json.dumps(metadata), params=payload, verify=False, headers=headers)
>>> print r
<Response [201]>
```

The new record is created (HTTP response code 201). The response text contains a success message and the newly created record's ID and location URI:
```python
>>> print r.text
{"record_id": 267, "message": "New record submitted for processing", "location": "/api/record/267"}
```

The record ID  `record_id` in the response message can directly be used to see the landing page of the newly created deposit: [267](https://trng-b2share.eudat.eu/record/267). If the page displays a restriction message, this is due the server-side processing of the ingestion. As soon as this is finished, the message will disappear.

### Check and display your results
Once the deposition process is completed, the results can be checked by requesting the record data using the new record ID. Follow the [record retrieval guide](01_Retrieve_existing_record.md) for an extensive description on how to do this.

In short, without explanation:
```python
>>> r = requests.get('https://trng-b2share.eudat.eu/api/record/267', params=payload, verify=False)
>>> print json.dumps(json.loads(r.text), indent=4)
{
    "files": [
        {
            "url": "https://trng-b2share.eudat.eu/record/267/files/sequence2.txt?version=1", 
            "name": "sequence2.txt", 
            "size": 3893
        }, 
        {
            "url": "https://trng-b2share.eudat.eu/record/267/files/sequence.txt?version=1", 
            "name": "sequence.txt", 
            "size": 292
        }
    ], 
    "domain": "generic", 
    "description": "My first dataset ingested using the API", 
    "contributors": [], 
    "creator": [], 
    "checksum": "91c0c0b3a55902f9b301d8291abe52260bd83458295f3fc43ca0259b65b78ea9", 
    "title": "My first dataset", 
    "publication_date": "", 
    "open_access": true, 
    "record_id": 267, 
    "version": "", 
    "alternate_identifier": "", 
    "licence": "", 
    "uploaded_by": "someone@somewhere.org", 
    "keywords": [], 
    "contact_email": "", 
    "resource_type": [], 
    "PID": "http://hdl.handle.net/11304/f5ef95b2-5443-4dc5-b85b-f8396f1d6b5e"
}
```
A persistent identifier (`PID` field) has been automatically generated and added to the metadata. Furthermore, a `checksum` has been calculated and the uploader's email address added in the `uploaded_by` field.

Unfortunately, some of the fields are empty. During the commit step, these fields were not added and therefore missing. It is highly recommended to complete all fields during this step in order to increase the discoverability, authenticity and reusability of the dataset.
