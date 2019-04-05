# Introduction
The B2HARE HTTP REST API can be used for interacting with B2SHARE via external services or applications, for example for integrating with other websites (research community portals) or for uploading or downloading large data sets that are not easily handled via a web browser. This API can also be used for metadata harvesting.

In the following introduction, the concepts of the use of the API is explained with regard to Python.

## Basic Concepts
A scientific community has the roles of creating and maintaining metadata schemas and curating the datasets which are part of a scientific domain or research project. B2SHARE users can be part of one or more communities. Some selected members of a community are also given the role of community administrators, which grants them the special rights needed for the schema definitions and record curation tasks. For information on how to retrieve community data from B2SHARE, refer to the [dedicated](03_List_communities.md) guide.

Any user can upload scientific datasets into B2SHARE and thus create data records. A record is comprised of data files and associated metadata. The record's metadata consists of a set of common fixed metadata fields and a set of custom metadata blocks, each block containing related metadata fields. A record is always connected to one scientific community which has the role of curating and maintaining it.

A data record can exist in several states. Immediately after creation a record enters the 'draft' state. In this state the record is only accessible by its owner and can be freely modified: its metadata can be changed and files can be uploaded into or removed from it. A draft can be published at any time, and through this action it changes its state from 'draft' to 'published', is assigned Persistent Identifiers, and becomes publicly accessible. Please note that the list of files in a published record cannot be changed. Refer to the [deposit guide](05_Create_new_deposit.md) to start depositing new records.

A record contains a set of common metadata fields and a set of custom metadata blocks. This metadata is not free form, however, but is governed by static schemas; the common metadata schema is set by B2SHARE and defines a superset of Dublin Core elements, while the schema for the custom metadata block is specific to each community and can be customized by the community administrators. The schemas are formally defined in the JSON Schema format. A special HTTP API call is available for retrieving the JSON Schema of a record in a specific community. In order to be accepted, the records submitted to a community must conform to the schema required by the community.

Refer to the [metadata update guide](06_Update_deposit_metadata.md) to alter metadata of existing records.

## Authentication
Certain API requests to the B2SHARE service require authentication, for example to create or modify draft records. Each such request to the server must provide an `access_token` parameter that identifies the user. The `access_token` is an opaque string which can be created in the user profile when logged in to the B2SHARE web user interface. B2SHARE's access tokens follow the OAuth 2.0 standard.

To obtain a personal access token follow the [token retrieval guide](00_Getting_your_access_token.md).

## HTTP requests
The HTTP requests are made using a URL with parameters targetting a specific service. Each URL consists of a protocol part (always 'https://'), a hostname and optionally a path. One of the following hostnames can be used to identify EUDAT's B2SHARE instances:

URL | Description
--- | -----------
`b2share.eudat.eu` | the hostname of the production site.
`trng-b2share.eudat.eu` | the base url of the training site. Use this URL for testing.

Using Python, a user can request all kinds of different data. For a quick start, refer to the [Testing your token](00_Getting_your_access_token.md#testing-your-token) guide.

### Variables in the descriptions
In the table below, the variables that can be used in the provided examples are listed.

Variable | Description
-------- | -----------
`community_id` | Identifier of a community defined in B2SHARE
`record_id` | Identifier for a specific record, which can be in draft or published state
`record_head_id` | Identifier for a group of records that are versions of each other
`schema_id` | Identifier for a metadata schema in B2SHARE
`file_bucket_id` | Identifier for a set of files. Each record has its own file set
`file_name` | Name of a file in a specific file bucket
`field_name` | Name of a metadata field of a metadata schema

Refer to the [Request and Metadata Reference Guide](B_Request_and_Metadata_Reference_Guide.md) appendix to see which requests are available and what metadata schemas and fields are supported.

### Request responses
In general, the following holds for HTTP request responses:
- All responses have a status code, for more information see [here](https://eudat.eu/services/userdoc/b2share-http-rest-api#status-codes).
- All response bodies are in JSON format and UTF-8 encoded.
- A record is represented as a JSON object: `{ "field1": value, … }`
- A collection of records is represented as a JSON array of objects: `[{ "field1": value, ... }, … ]}`
- Timestamps are in UTC and formatted according to ISO 8601: `YYYY-MM-DDTHH:MM:SS+00:00`

If your target service does not have a proper certificate installed, in many cases you will get a warning about insecure connections through HTTPS when turning off certificate verification in the request statement (`verify=False`):

```python
/usr/lib/python2.7/dist-packages/urllib3/connectionpool.py:732: InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.org/en/latest/security.html (This warning will only appear once by default.)
  InsecureRequestWarning)
```

You can ignore this. If you want to get rid of it, use the following Python code to do so:

```python
>>> import
>>> requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
```

### Errors
If your request fails with an HTTP response code 401, you need to update your access token on the B2SHARE website. If your request was not accepted an error response will be returned which looks similar to this:

```python
{
  "message": "The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.",
  "status": 404
}
```

In this case, the requested objet was not found and a `404` status code was returned.

## A publication workflow

The HTTP API does not impose a specific workflow for creating a record. The following example workflow only defines the most basic steps:

1. Identify a target community for your data by following the HTTP API [List all communities](03_Communities.md#list-all-communties) guide
1. Using the community's identifier, retrieve the community's JSON Schema of the record's metadata. The submitted metadata will have to conform to this schema. Use the [Get community schema](03_Communities.md#get-community-metadata-schema) guide to achieve this
1. Create a draft record: follow the [Create draft record](05_Create_new_record.md) guide to create a draft record with initial metadata in it
1. [Upload files](05_Create_new_record.md#add-files-to-your-new-draft-record) into the draft record
1. Set the [complete metadata](05_Create_new_record.md#add-additional-metadata-to-your-draft-record) and publish the record
