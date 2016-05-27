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

A response text contains one or more fields in a serialized [JSON](http://www.json.org/) structure string. Each field has a specific [JSON data type](https://en.wikipedia.org/wiki/JSON#Data_types.2C_syntax_and_example). The text does not define a JSON schema to which the text can be validated to.

For a deposition, the following fields will be returned:
Field name | JSON data type | Description
---------- | -------------- | -----------
record_id | Number | Deposition unique ID number
authors | String | Creator's full name (comma separated if more available)
title | String | Name
description | String | Description 
domain | String | Scientific domain
date | String | Deposit date
pid | String | Persistent identifier
email | String | Email address of depositor (not creator)
file_url | String | URL of deposited files
license | String | License
files | Object array | Deposited files (see below)

The `files` field is a JSON structure on itself:
Field name | JSON data type | Description
---------- | -------------- | -----------
full_name | String | 
url | String | 
size | Number | 