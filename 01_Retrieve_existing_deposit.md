# Retrieving an existing deposit
In this guide module the retrieving of specific deposits will be explained. Using the information of a deposit or record, the corresponding files, metadata and other information can be used to automate data processing and transfer complete deposits to other services. For the B2SHARE service a record is the equivalent of a deposit and therefore these two terms are used interchangeably.

### Setup your connection
Please make sure your machine has been properly set up to use Python and required packages. Follow [this](A_Setup_and_install.md) guide in order to do so.

This guide assumes you have successfully registered your account on the [B2SHARE website](https://trng-b2share.eudat.eu) using your institutional credentials or social ID through B2ACCESS.

### Request the deposit
To retrieve a specific record, the record ID of that deposit is required and needs to be sent through the API as well. In Python, the URL where the request is sent to, needs to be extended with the record ID.

First, the token is read from file in a Python session:
```python
>>> f = open(r'token', 'r')
>>> token = f.read()
```

Then, the request is set up:
```python
>>> import requests
>>> r = requests.get('https://trng-b2share.eudat.eu/api/record/1', params={'access_token': token}, verify=False)
```
Most likely you will get a warning about insecure connections through HTTPS. You can ignore that for now.

To verify whether the request succeeded and see the result, print the variable `r`:
```python
>>> print r
<Response [200]>
>>> print r.text
{"files": [{"url": "https://trng-b2share.eudat.eu/record/1/files/c33a933c-8202-11e3-92a1-005056943408.zip?version=1", "name": "c33a933c-8202-11e3-92a1-005056943408.zip", "size": 549252}], "domain": "linguistics", "description": "This is a small sample dataset from PDT 2.0. As such it can be released under a very permissive CC-BY license.", "contributors": [], "creator": ["Haji\u010d, Jan"], "checksum": "c5450f4822ee3ff6a6c8c0a400c8ca5294770fb115e55b7aa70c5b9d116a0043", "title": "Prague Dependency Treebank 2.0 Sample Data", "alternate_identifier": "", "open_access": true, "keywords": ["treebank", "sample"], "version": "", "contact_email": "", "licence": "CC-BY 4.0", "uploaded_by": "stranak@ufal.mff.cuni.cz", "record_id": 1, "publication_date": "20-01-2014", "domain_metadata": {"quality": "release", "region": "Czechia", "project_name": "", "ling_resource_type": ["treebank"], "language_code": "ces Czech"}, "resource_type": [], "PID": "http://hdl.handle.net/11113/1986e7ae-8203-11e3-8cd7-14feb57d12b9"}
```

### Display your deposit
To improve the readability, use the JSON package:
```python
>>> import json
>>> result = json.loads(r.text)
>>> print json.dumps(result, indent=4)
{
    "files": [
        {
            "url": "https://trng-b2share.eudat.eu/record/1/files/c33a933c-8202-11e3-92a1-005056943408.zip?version=1", 
            "name": "c33a933c-8202-11e3-92a1-005056943408.zip", 
            "size": 549252
        }
    ], 
    "domain": "linguistics", 
    "description": "This is a small sample dataset from PDT 2.0. As such it can be released under a very permissive CC-BY license.", 
    "contributors": [], 
    "creator": [
        "Haji\u010d, Jan"
    ], 
    "checksum": "c5450f4822ee3ff6a6c8c0a400c8ca5294770fb115e55b7aa70c5b9d116a0043", 
    "title": "Prague Dependency Treebank 2.0 Sample Data", 
    "publication_date": "20-01-2014", 
    "open_access": true, 
    "record_id": 1, 
    "version": "", 
    "alternate_identifier": "", 
    "licence": "CC-BY 4.0", 
    "uploaded_by": "stranak@ufal.mff.cuni.cz", 
    "keywords": [
        "treebank", 
        "sample"
    ], 
    "contact_email": "", 
    "domain_metadata": {
        "ling_resource_type": [
            "treebank"
        ], 
        "region": "Czechia", 
        "project_name": "", 
        "quality": "release", 
        "language_code": "ces Czech"
    }, 
    "resource_type": [], 
    "PID": "http://hdl.handle.net/11113/1986e7ae-8203-11e3-8cd7-14feb57d12b9"
}
```
Our request was successfull and we now have all the information to process the deposit and its metadata and files.

#### Getting specific metadata values
To display specific information from the metadata, simply add the field name as an index to the `result` variable. For example, to solely display the checksum, do the following:
```python
>>> print result["checksum"]
c5450f4822ee3ff6a6c8c0a400c8ca5294770fb115e55b7aa70c5b9d116a0043
```

Similarly, the file name of the first file can be displayed using an additional numerical index on the `files` key followed by the `name` index:
```python
>>> print result["files"][0]["name"]
c33a933c-8202-11e3-92a1-005056943408.zip
```

### Downloading a deposit file
In many cases, the corresponding files are needed to allow further processing of the data contained. A simple loop allows to get all files and store them at a specific location. Since all files are publically accessible, no authentication is required by token used earlier.

To avoid overwriting any existing files, a specific download folder is created in the current working directory using the Python package `os`:
```python
>>> import os
>>> os.mkdir('download')
```

Using the `urllib` package, files can be directly downloaded by URL:
```python
>>> import urllib
>>> for f in result["files"]:
...     urllib.urlretrieve(f["url"], "download/" + f["name"])
... 
(u'download/c33a933c-8202-11e3-92a1-005056943408.zip', <httplib.HTTPMessage instance at 0x10ca86098>)
```
