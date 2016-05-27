# Request and Metadata Reference Guide
This guide will list the possibilities regarding API requests and metadata options.

### General information
API requests in Python can be done using the Python [requests](http://docs.python-requests.org/en/master/) package. The package is non part of the standard Python download and therefore needs to be [installed](A_Setup_and_install.md#Packages). 

Before it can be used in your scripts and commands, it needs to be loaded:
```python
>>> import requests
```

### Request methodology in Python
Each request by default needs three parameters: the URL


#### Available parameters


### API interaction using curl

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
title | String | Name | 

The following fields are also included

Field name | JSON data type | Description
---------- | -------------- | -----------
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
url | String | 
size | Number | 