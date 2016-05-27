# Request and Metadata Reference Guide
This guide will list the possibilities regarding API requests and metadata options.

### General information
API requests in Python can be done using the Python [requests](http://docs.python-requests.org/en/master/) package. The package is non part of the standard Python download and therefore needs to be [installed](A_Setup_and_install.md#Packages). 

Before it can be used in your scripts and commands, it needs to be loaded:
```python
>>> import requests
```

### Request methodology in Python
Each request by default needs at least one parameter, the URL pointing to the object of which the information is requested. In addition, several optional parameters can be added providing for example authentication information, request header and verification.

The returned object contains a lot of information which can be extracted using the object methods and variables provided. For example, a typical record retrieval request would look like this:
```python
>>> r = requests.get('https://trng-b2share.eudat.eu/api/record/267', params={'access_token': token}, verify=False)
>>> print r.json()["files"][0]
{u'url': u'https://trng-b2share.eudat.eu/record/267/files/sequence2.txt?version=1', u'name': u'sequence2.txt', u'size': 3893}
```
The latter command displays the first file contained in the record.

#### Available parameters
Several parameters can be added to any request.

Parameter | Data type | Description
--------- | --------- | -----------
params | Dictionary | Additional necessary information like the authentication token
data | String | Additional request data, like upload file information
headers | Dictionary | HTTP request header information, like response text formatting
verify | Boolean | Indication whether verification needs to be performed

Note that the `data` parameter needs a string as data, and therefore any dictionary needs to be flattened before it can be send as a data parameter.

### Response fields
All requests made to B2SHARE will return a response code and text. The response code equals one of the standardized HTTP response codes, indicating the success or failure of the request. An overview of these codes can be found on [Wikipedia](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes).

A response text contains one or more fields in a serialized [JSON](http://www.json.org/) structure string, of which each field has a specific [JSON data type](https://en.wikipedia.org/wiki/JSON#Data_types.2C_syntax_and_example). The text does not define a JSON schema to which the text can be validated to.

For a deposition, the most important fields that are returned are:

Field name | JSON data type | Description | Default value
---------- | -------------- | ----------- | -------------
authors | String | Creator's full name (comma separated if more available)
checksum | String | Checksum of all data | Hexidecimal string
creator | String array | Creator(s) of data set | Empty array
date | String | Deposit date |
description | String | Deposit description |
domain | String | Scientific domain |
files | Object array | Deposited files (see below) | Empty array
licence | String | License | 
open_access | Boolean | Open access | True
PID | String | URL containing the persistent identifier (PID)
publication_date | String | Date of publication of data set | 
record_id | Number | Deposition unique ID number | Automatic
title | String | Deposit title | 

The following fields are also included

Field name | JSON data type | Description | Default value
---------- | -------------- | ----------- | -------------
alternate_identifier | String | Other identifier | 
contributors | String array | Mentionable contributors | Empty array
contact_email | String | Contact email address |
keywords | String | Tags describing deposit | Empty array
resource_type | String | File format(s) of files | Empty array
uploaded_by | String | Original uploader of content | Uploader's email address
version | String | Version of deposit |

The `files` field is a JSON structure on itself:

Field name | JSON data type | Description
---------- | -------------- | -----------
full_name | String | File name with extension
url | String | Full URL for file retrieval
size | Number | File size in bytes

### API interaction using curl
Using command-line interfaces any of the information stored in the B2SHARE service can be retrieved as well. A commonly-used tool is curl.