# Create a new deposit
When your dataset is ready for publication, it can be uploaded to the B2SHARE service by creating a deposition and adding files and metadata. This submodule will guide you through the creation process of new depositions. It covers the actual creation of a new record, the addition of files and metadata and the final completion.

Please note that the B2SHARE service makes a distinction between the two terms `record` and `deposition`. A record is unchangeable and has a persistent identifier (PID) assigned to it. A user can create a record by first creating a deposition, which is modifiable. Files and metadata can be placed into a deposition, but not into a record.

### Setup your connection
Please make sure your machine has been properly set up to use Python and required packages. Follow [this](A_Setup_and_install.md) guide in order to do so.

This guide assumes you have successfully registered your account on the [B2SHARE website](https://trng-b2share.eudat.eu) using your institutional credentials or social ID through B2ACCESS. In addition, the loading of the token, importing Python packages and checking request responses will not be covered here.

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

Response code 201 indicates the deposition has been successfully created. The deposition ID in the response text is used to identify the deposition during the additional steps of adding files and metadata:
```python
>>> result = json.loads(r.text)
>>> print result["deposit_id"]
```

### Add files to your new deposit
After creation of the deposition, files need to be added. This is achieved in a similar way as during the creation step by posting a request. Make sure your data files are accessible in the Python session. In this case the files named `sequence.txt` and `sequence2.txt` are added to the deposition.

First, define a dictionary which contains Python open calls to the files. Files are added one-by-one:
```python
>>> files = {'file': open('sequence.txt', 'rb')}
```
In this statement, the action of opening the file is not actually performed. Only when the request call is performed, files will be read.

Define the request URL by adding the deposition ID and `files` end point:
```python
>>> url = 'https://trng-b2share.eudat.eu/api/deposition/' + result["deposit_id"] + '/files'
>>> payload = {'access_token': token}
```

The complete request looks as follows:
```python
>>> r = requests.post(url, files=files, params=payload, verify=False)
```

When the request is successfull, the result can be checked:
```python
>>> print r
<Response [200]>
>>> print r.text
{"files": [{"name": "sequence.txt"}], "message": "File(s) saved"}
```

When not successfull, check the error by displaying the response text, for example when the deposition is not found:
```
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

### Commit the changes
The final step will complete the deposition by adding metadata and committing it.

### Check and display your results
