# Request and Metadata Reference Guide
This reference guide lists the possibilities regarding API requests and metadata options.

### General information
API requests in Python can be done using the Python [requests](http://docs.python-requests.org/en/master/) package. The package is not part of the standard Python download and therefore needs to be [installed](A_Setup_and_install.md#Packages).

Before it can be used in your scripts and commands, it needs to be loaded:
```python
>>> import requests
```

The base URL for all API calls is `https://trng-b2share.eudat.eu/api/' with an additional URI appended (see below).

### Quick reference table
A request can be made using a HTTP request method, such as `GET` or `POST`. No other HTTP request methods are currently supported by the B2SHARE service.

For all requests there are optional parameters which need to be added in order to take effect. The only required parameter is the `access_token`. See the table in the 'Parameter variables' section for a complete overview.

For post method requests, additional non-parameter data can be sent along with the request.

Request | HTTP method | URI | Optional | Return value
------- | ----------- | --- | -------- | ------------
List all records | GET | `records` | `page_size`, `page_offset` | List of records (in JSON format)
List records per community | GET | `records/<community_name>` | `page_size`, `page_offset` | List of records (in JSON format) or an error message with the list of valid community identifiers if the `community_name` is invalid
List specific record | GET | `record/<record_id>` | | A JSON-formatted string containing the record's metadata and files
Create deposition | POST | `depositions` | | URL of the deposition (both as JSON and in the field 'Location' in the http header)
Add file to deposition | POST | `deposition/<deposition_id>/files` | file (as multipart/form-data) | Name and size of the newly uploaded file
List deposition files | GET | `deposition/<deposition_id>/files` | | Name and size of all the files in the deposition object
Commit deposition | POST | `deposition/<deposition_id>/commit` | metadata, header | Location URL of the new record if the submitted metadata is valid; otherwise, the list of all the metadata fields that can be filled in and details on each one

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
Several parameters can be added to any request. Please note that the parameters only function for relevant HTTP request methods. The most important are:

Parameter | Data type | Description
--------- | --------- | -----------
params | Dictionary | Additional necessary information like the authentication token
files | Dictionary | Files to be transfered
data | String | Additional request data, like metadata
headers | Dictionary | HTTP request header information, like response text formatting
verify | Boolean | Indication whether verification needs to be performed

All parameters need a dictionary as value with the exception of the `data` parameter which requires a string. For the latter therefore any dictionary needs to be serialized to a string before it can be send as the value for the data parameter. This can be done using the JSON Python package.

#### Parameter variables
The `params` parameter for a request can contain several variables with their corresponding values. All values are of the string data type.

Variable | Description
-------- | -----------
access_token | Access token used for authentication
community_name | Name of the user community in B2SHARE
page_offset | Page offset for paginated output data
page_size | Size of a page in case pagination is used
record_id | Identifier for a specific record
deposition_id | Identifier for a specific deposition

The only mandatory variable is `access_token`, in case authentication is required. The rest of the variables are optional.

### Response fields
All requests made to B2SHARE will return a response code and text. The response code equals one of the standardized HTTP response codes, indicating the success or failure of the request. An overview of these codes can be found on [Wikipedia](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes).

A response text contains one or more fields as a [JSON](http://www.json.org/) object serialized into a string (UTF-8 encoded). Each field has a specific [JSON data type](https://en.wikipedia.org/wiki/JSON#Data_types.2C_syntax_and_example). The response body does not define a JSON schema to which the text can be validated to.

All timestamps are in UTC and formatted according to [ISO 8601](http://www.iso.org/iso/home/standards/iso8601.htm): `YYYY-MM-DDTHH:MM:SS+00:00`

For an existing deposit (or record), the most important fields that are returned are:

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

The following fields can also be included:

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

A collection of deposits is represented as a JSON array of objects.

### API interaction using curl
Using command-line interfaces any of the information stored in the B2SHARE service can be retrieved as well using similar requests. A commonly-used tool is [curl](https://curl.haxx.se/). Refer to the Quick reference table section for a complete list of the various requests together with their options and return value. For curl commands, optional parameters are added to the URL, while non-parameter options are added as options in the command.

In general, a curl command to send a request to a service is constructed as follows:
```sh
curl [options...] <url>
```
For the B2SHARE training instance, this becomes:
```sh
curl [-i] [-X <method>] [-H "Content-Type: application/json"] [-F file=@<filename>]
    [-d '{"key":"value"}'] 'https://trng-b2share.eudat.eu/api/<URI>?<parameters>'
```
where all text between brackets is optional. For `method` either `GET` (default) or `POST` can be put and `URI` is one of the URIs listed in the table. Optionally, you can add `-i` to return header information, `-F` to send form data (i.e. files), `-d` to send additional data (i.e. metadata) and/or `-H` to set the return string format. These might be required when using some specific post requests during deposition. The parameters field is an ampersand-separated list of key-value pairs, e.g. `access_token=123123&page_offset=2`.

### HTTP response codes

To make sure the request has been successful, always check the HTTP reponse code of a request. In this section, any errors generated by Python itself are not dealed with.

#### Checking your request response

Using the requests package of Python, all requests can be checked whether they succeeded by printing the object containing the request:

```python
>>> r = requests.get('https://trng-b2share.eudat.eu/api/records')
>>> print r
<Response [200]>
```

The request was successful. However, this does not guarantee that the information was found which was originally requested.

#### Erroneous requests
There can be several reasons why a requests didn't succeed. In general, the first occuring error is returned and can therefore be investigated.

For example, when a non-existing API endpoint is used as the path in the request, HTTP response code 404 is returned:

```python
>>> r = requests.get('https://trng-b2share.eudat.eu/api/drafts', verify=False)
>>> print r.text
{
  "message": "The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.",
  "status": 404
}
```

Or when a unknown identifier is used for a record:
```python
>>> r = requests.get('https://trng-b2share.eudat.eu/api/records/test', params=payload, verify=False)
>>> print r.text
{"status": 404, "message": "PID does not exist."}
```
