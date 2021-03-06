# Request and Metadata Reference Guide
This reference guide lists the possibilities regarding API requests and metadata options.

### General information
API requests in Python can be done using the Python [requests](http://docs.python-requests.org/en/master/) package. The package is not part of the standard Python download and therefore needs to be [installed](A_Setup_and_install.md#Packages).

Before it can be used in your scripts and commands, it needs to be loaded:
```python
>>> import requests
```

The base URL for all API calls is `https://trng-b2share.eudat.eu/api/` with an additional URI appended (see below).

All text-based request payloads and returned responses are encoded in JSON. Therefore a JSON package that can handle these data for you are necessary. Most commonly used are the `simplejson` or `json` packages.

#### Important note
The service expects the API request to have a trailing slash ('/') at the end of the URI, but before any parameters. Your browser and the requests Python package will automatically add this character, though when using curl (see [below](#api-interaction-using-curl)) you must make sure to add it otherwise the request will fail.

### Request reference table
A request can be made using a HTTP request method, such as `GET` or `POST`.

For all requests there are optional parameters which need to be added in order to take effect. The parameter `access_token` is required for creating or modifying records and to retrieve private or community-only records. See the table in the 'Parameter variables' section for a complete overview.

For post method requests, additional non-parameter data can be sent along with the request.

Request | HTTP method | Full URI | Return value
------- | ----------- | -------- | ------------
[List all records (search)](02_List_existing_records.md#retrieve-a-list-of-records) | GET | `/api/records` | List of records
[List your draft records (search)](02_List_existing_records.md#retrieve-a-list-of-your-draft-records) * | GET | `/api/records?drafts` | List of records
[List specific record](01_Retrieve_existing_record.md#get-details-of-a-specific-record) | GET | `/api/records/<record_id>` | A JSON-formatted string containing the record's metadata and files
[List specific draft record](01_Retrieve_existing_record.md#get-details-of-a-specific-record) | GET | `/api/records/<record_id>/draft` | A JSON-formatted string containing the draft record's metadata and files
[Download file from record](01_Retrieve_existing_record.md#downloading-files-from-a-record) | GET | `/api/files/<file_bucket_id>/<filename>` | A JSON-formatted string containing the draft record's metadata and files
[List communities](03_Communities.md#list-communities) | GET | `/api/communities` | List all communities and their metadata
[List records per community](03_Communities.md#retrieve-community-specific-records) | GET | `/api/records/<community_id>` | List of records of a specific community
[Get community schema](03_Communities.md#get-community-metadata-schema) | GET | `/api/records/<community_id>/schemas/<version>` | Get the schema of a specific community
[Create draft record](05_Create_new_record.md#create-a-new-draft-record) * | POST | `/api/records` | Create a new draft record, requires metadata payload
[Upload file into draft record](05_Create_new_record.md#add-files-to-your-new-draft-record) * | PUT | `/api/files/<file_bucket_id>/<filename>` | Add file to draft record, requires file name and bucket identifier
[Delete file from draft record](05_Create_new_record.md#delete-a-file-from-a-draft-record) * | DELETE | `/api/files/<file_bucket_id>/<filename>` | Remove a file from a draft record's file bucket
[List uploaded files of record](05_Create_new_record.md#check-your-uploaded-files) * | GET | `/api/files/<file_bucket_id>` | List the file uploaded into a record object, requires file bucket identifier
[Update record's metadata](05_Create_new_record.md#add-metadata-to-your-draft-record) * | PATCH | `/api/records/<record_id>` | Update a published record's metadata with new metadata, requires metadata in the form of a JSON Patch
[Update draft record's metadata](06_Update_record_metadata.md#updating-metadata) * | PATCH | `/api/records/<record_id>/draft` | Update (draft) record's metadata with new metadata, requires metadata in the form of a JSON Patch
[Update community-specific fields](06_Update_record_metadata.md#updating-community-specific-fields) * | PATCH | `/api/records/<record_id>/draft` | Update (draft) record's community-specific metadata with new or updated information in the form of a JSON Patch
[Update multivalue fields](06_Update_record_metadata.md#updating-multivalue-fields) * | PATCH | `/api/records/<record_id>/draft` | Update draft record's multivalue metadata fields with new or updated information in the form of a JSON Patch
[Create a new version of an existing published record](08_Record_versioning.md#creating-a-new-draft-record-from-an-existing-published-record) * | POST | `/api/records` | Create a new draft record based on an existing published record. Requires the `version_of` parameter with the `<record_id>` of the published record as value
[Get record versions](08_Record_versioning.md#get-all-record-versions) | GET | `/api/records/<record_id>/versions` | Get a listing of all record versions of a dataset
[Get statistics](10_Special_requests.md#get-the-statistics-of-a-record) | POST | `/api/stats` | Get specific statistics about one or more records or other objects, requires specific JSON data object
[Submit draft record for publication](05_Create_new_record.md#publishing-your-draft-record) * | PATCH | `/api/records/<record_id>` | Change status of record, requires JSON Patch with value of `publication_state` field specified
[Get user information](10_Special_requests.md#listing-user-information) * | GET | `/api/user` | List information in your user account
[Report record as abusive](10_Special_requests.md#report-a-record-as-an-abuse-record) * | POST | `/api/records/<record_id>/abuse` | Report a record as an abuse record, requires specific JSON object with information
[Request access to data in a record](10_Special_requests.md#send-a-request-to-get-access-to-restricted-data-in-a-record) * | POST | `/api/records/<record_id>/accessrequests` | Send a request to get access to restricted data in a record, requires specific JSON data object with information
[Delete draft record](10_Special_requests.md#delete-a-draft-record) * | DELETE | `/api/records/<record_id>/draft` | Delete a draft record
[Delete published record](10_Special_requests.md#delete-a-published-record) ** | DELETE | `/api/records/<record_id>` | Delete a published record

\* requires authentication using your access token

\*\* requires site administrator priviledges and authentication using your access token

### Request methodology in Python
Each request by default needs at least one parameter, the URL pointing to the object of which the information is requested. In addition, several optional parameters can be added providing for example authentication information, request header and verification.

The returned object contains a lot of information which can be extracted using the object methods and variables provided. For example, a typical record retrieval request would look like this:

```python
>>> r = requests.get('https://trng-b2share.eudat.eu/api/records/a1c2ef96a1e446fa9bd7a2a46d2242d4', params={'access_token': token})
>>> print(r.json())
```

The latter command displays the retrieved metadata parsed by a JSON interpreter as a dictionary (depending on your browser and settings).

#### Available parameters
Several parameters can be added to any request. Please note that the parameters only function for relevant HTTP request methods. The most important are:

Parameter | Data type | Description
--------- | --------- | -----------
`params` | Dictionary | Additional necessary information like the authentication token
`files` | Dictionary | Files to be transfered
`data` | String | Additional request data, like metadata
`headers` | Dictionary | HTTP request header information, like response text formatting
`verify` | Boolean | Indication whether verification needs to be performed

All parameters need a dictionary as value with the exception of the `data` parameter which requires a string. For the latter therefore any dictionary needs to be serialized to a string before it can be send as the value for the data parameter. This can be done using the JSON Python package.

#### Parameter variables
The `params` parameter for a request can contain several variables with their corresponding values. All values are of the string data type.

Variable | Description
-------- | -----------
`access_token` | Access token used for authentication
`community_id` | Identifier of the community in B2SHARE
`page` | Page offset for paginated output data
`size` | Size of a page in case pagination is used
`record_id` | Identifier for a specific record
`drafts` | Indicator to return draft records only

The variable `access_token` is mandatory for creating or modifying existing records. The other variables are optional.

### Response fields
All requests made to B2SHARE will return a response code and text. The response code equals one of the standardized HTTP response codes, indicating the success or failure of the request. An overview of these codes can be found on [Wikipedia](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes).

A response text contains one or more fields as a [JSON](http://www.json.org/) object serialized into a string (UTF-8 encoded). Each field has a specific [JSON data type](https://en.wikipedia.org/wiki/JSON#Data_types.2C_syntax_and_example). The response body does not define a JSON schema to which the text can be validated to.

All timestamps are in UTC and formatted according to [ISO 8601](http://www.iso.org/iso/home/standards/iso8601.htm): `YYYY-MM-DDTHH:MM:SS+00:00`

Every record has the following metadata structures:

Name | Description
---- | -----------
`created` | Date and time the record was created
`files` | All files attached to the record
`id ` | Unique identifier of the record
`links` | List of URLs that point to the record or related resources
`metadata` | All metadata belonging to the record
`updated` |

The most important fields in the metadata structure that are returned when they have actual values:

Field name | JSON data type | Description | Default value
---------- | -------------- | ----------- | -------------
`$schema` | URL | Resource locator pointing to the metadata schema used when creating the record | Any valid schema URL
`community` | String | Community identifier | One of the known community identifiers
`title` | Array of strings | Record title(s) |
`descriptions` | Array of objects | Record descriptions |
`creators` | Array of strings | Creators of dataset in record |
`open_access` | Boolean | Open access | True
`publication_date` | String | The date when the data was or will be made publicly available (e.g. 1971-07-13) |
`licence` | String | License under which the data in the record can be used |
`keywords` | Array of strings | A list of keywords or key phrases describing the resource in the record |
`contact_email` | String | Email address of contact person for dataset |
`date` | String | Deposit date |
`publication_state` | String | Date of publication of data set | 'draft'

For published records, the following fields are present:

Field name | JSON data type | Description
---------- | -------------- | -----------
`DOI` | String | Globally resolvable unique identifier registered by a DOI service
`ePIC_PID` | String | Globally resolvable unique identifier registered by a EPIC PID service

The following fields are included when they are set:

Field name | JSON data type | Description | Default value
---------- | -------------- | ----------- | -------------
`alternate_identifier` | String | Other identifier |
`contributors` | String array | Mentionable contributors | Empty array
`resource_type` | String | File format(s) of files | Empty array
`version` | String | Version of deposit |

The `files` field is a JSON structure on itself and contains information about the attached files:

Field name | JSON data type | Description | Example
---------- | -------------- | ----------- | -------
`bucket` | String | Identifier of file bucket that contains the file | `93de120a-f134-439f-a1d4-473427e2f5b2`
`checksum` | String | Cryptographic hash function result calculated from file data | `md5:5ca7e5c2b882a6099f8b9f7a62c6d760`
`ePIC_PID ` | URL | Unique URL pointing to the file | http://hdl.handle.net/11304/7db9150a-4fd7-4bce-9a1f-e2f59ffdd2c7
`key` | String | File name of the file | `data.tar.gz`
`size` | Integer | Size of the data contained in file | `5441275460`
`version_id` | String | Version identifier belonging to currently stored file | `a0603720-53b4-471d-9c7b-e7ee727bb3d0`

### Collections of objects
A collection of records or communities is represented as a JSON structure with at least the following fields:

Field name | JSON data type | Description | Default value
---------- | -------------- | ----------- | -------------
`hits` | Object | Actual result of the request or query |
`links` | Object | URLs to the current result and related results, such as the next page when querying records |

### API interaction using curl
Using command-line interfaces any of the information stored in the B2SHARE service can be retrieved as well using similar requests. A commonly-used tool is [curl](https://curl.haxx.se/). Refer to the Quick reference table section for a complete list of the various requests together with their options and return value. For curl commands, optional parameters are added to the URL, while non-parameter options are added as options in the command.

In general, a curl command to send a request to a service is constructed as follows:
```sh
curl [options...] <url>
```
For the B2SHARE training instance, this becomes:
```sh
curl [-i] [-X <method>] [-H "Content-Type: application/json"] [-d @<filename> | -d '{"key":"value"}']
        'https://trng-b2share.eudat.eu<URI>?<parameters>'
```

where any bracketed option is optional. For `method` either `GET` (default), `POST`, `PUT`, `PATCH` or `DELETE` can be put and `URI` is one of the URIs listed in the [table](#request-reference-table). Optionally, you can add `-i` to return header information. Use the `-d` option to send files or metadata. Use the `-H` option to add headers to the request to e.g set the return string format. These might be required when using some specific post requests during record. The parameters field is an ampersand-separated list of key-value pairs, e.g. `access_token=123123&page=2`.

### HTTP response codes
To make sure the request has been successful, always check the HTTP reponse code of a request. In this section, any errors generated by Python itself are not dealed with.

#### Checking your request response
Using the requests package of Python, all requests can be checked whether they succeeded by printing the object containing the request:

```python
>>> r = requests.get('https://trng-b2share.eudat.eu/api/records')
>>> print(r)
<Response [200]>
```

The request was successful. However, this does not guarantee that the information was found which was originally requested, see the contents of the body of the response for the actual data.

#### Erroneous requests
There can be several reasons why a request didn't succeed. In general, the first occuring error is returned and can therefore be investigated.

For example, when a non-existing API endpoint is used as the path in the request, HTTP response code 404 is returned:

```python
>>> r = requests.get('https://trng-b2share.eudat.eu/api/drafts')
>>> print(r.text)
{
  "message": "The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.",
  "status": 404
}
```

Or when a unknown identifier is used for a record:
```python
>>> r = requests.get('https://trng-b2share.eudat.eu/api/records/non-existing-record-identifier')
>>> print(r.text)
{"message": "PID does not exist.", "status": 404}
```

Or when authentication is required, but not given:
```python
>>> r = requests.get('https://trng-b2share.eudat.eu/api/records?drafts')
>>> r.text
{"message": "Only authenticated users can search for drafts.", "status": 401}
```

When provided metadata is incorrectly structured or valued:
```python
>>> patch = [{"path": "/titles", "value": [{"title": "Some title"}, {"title": "Some title"}], "op": "add"}]
>>> r = requests.patch('https://trng-b2share.eudat.eu/api/records/9e2f1bfa34ca402c96ff37b201b1a3ba/draft', data=simplejson.dumps(patch), params=params, headers=header)
>>> print(r.json())
{'message': 'Validation error.', 'errors': [{'message': "[{'title': 'Some title'}, {'title': 'Some title'}] has non-unique elements", 'field': 'titles'}], 'status': 400}
```
