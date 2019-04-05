# Special requests
In this guide more specific API calls are explained, like reporting abuse and getting access to restricted data. As the B2SHARE REST API continuously expands with new functionality, please check back later to find out new options.

The guide currently covers:
- Listing information about your user
- Reporting a record as an abuse record
- Sending a request to get access to restricted data in a record
- Getting the statistics of a record
- Deleting draft records
- Deleting published records

### Setup your connection
Please make sure your machine has been properly set up to use Python and required packages. Follow [this](A_Setup_and_install.md) guide in order to do so.

This guide assumes you have successfully registered your account on the [B2SHARE website](https://trng-b2share.eudat.eu) using your institutional credentials or social ID through B2ACCESS. In addition, the loading of the token, importing Python packages and checking request responses will not be covered here.

## Listing user information
B2SHARE keeps track of your personal information, including your email address, name and local identifier. If you have been assigned specific roles in communities or somewhere else, this is stored in B2SHARE as well.

To see your information and roles, use the following request with your access token:

```python
>>> params = {"access_token": token}
>>> r = requests.get("https://trng-b2share.eudat.eu/api/user", params=params)
```

```python
>>> print(r.text)
{
  "email": "<your email address>",
  "id": 10,
  "name": "<your name>",
  "roles": [
    {
      "description": "Member role of the community \"Community 1\"",
      "id": 2,
      "name": "com:8fa83d0775212c4234f93da964d2fa2c:member"
    },
    {
      "description": "Member role of the community \"Community 2\"",
      "id": 36,
      "name": "com:fba2881fb04d0a9bcf2e759f6e6fe48e:member"
    },
    {
      "description": "Admin role of the community \"Community 2\"",
      "id": 35,
      "name": "com:fba2881fb04d0a9bcf2e759f6e6fe48e:admin"
    }
  ]
}
```

In this response, the email address and name of your user are visible as well as three different roles. This user is a member of 'Community 1' and 'Community 2', as well as a community administrator for community 'Community 2'.

If you are a community administrator, you can [list all submitted draft records](02_list_existing_records.md#list-all-submitted-draft-records-of-a-community) of your community that are ready for review.

## Report a record as an abuse record
If you find anything wrong with an existing published record that is not your own, you can report the record using the API. When the request is successfully done, the administrator of the community will receive an automatic e-mail in which the abuse is reported.

Currently, four different reasons for abuse are defined of which one should be included in the report (see table below).

Tag | Label | Description
--- | ----- | -----------
`noresearch` | Abuse or Inappropriate content |  The record contains material that is abusively used by the creator of the record, or the record contains inappropriate material
`copyright` | Copyrighted material | The record contains copyrighted material not owned by the record's creator
`noresearch` | Not research data | The record does not contain any research data
`illegalcontent` | Illegal content | The record contains other illegal content

Furthermore, the reporter and an additional message are included in the API request. In this example, the record `b43a0e6914e34de8bd19613bcdc0d364` is reported for abuse because it does not contain research data. The reason is indicated by setting the corresponding tag to `true` in the data structure. Multiple reasons can be set at the same time. The reporter's personal and address information are included to allow any contact after the report.

```python
>>> header = {"Content-Type": 'application/json'}
>>> data = {"noresearch": True,
            "abusecontent": True,
            "copyright": False,
            "illegalcontent": False,
            "message": "This record does not contain any research data...",
            "name": "John Smith",
            "affiliation": "Some University",
            "email": "j.smith@example.com",
            "address": "Example street",
            "city": "ExampleCity",
            "country": "ExampleCountry",
            "zipcode": "12345",
            "phone": "07364017452"
           }
>>> params = {"access_token": token}
```

The header is used to indicate that the payload is in JSON format. To make the request, the `abuse` indicator is added to the URL, and the data structure is provided as a serialized string. The POST request then looks as follows:

```python
>>> url = "https://trng-b2share.eudat.eu/api/records/b43a0e6914e34de8bd19613bcdc0d364/abuse"
>>> r = requests.get(url, params=params, data=json.dumps(data), headers=header)
```

If the request is successful, the response looks as follows:

```python
>>> print(r)
<Response [200]>
>>> print(r.text)
{
  "message": "The record is reported."
}
```

Please note that in all cases you have to provide all abuse reasons at the same time, but only one can be set to `true`. If you have two or more set to `true` the following response will be returned:

```python
>>> print(r)
<Response [400]>
>>> print(r.text)
{
  "Error": "From 'noresearch', 'abusecontent', 'copyright', 'illegalcontent' (only) one should be True"
}
```

## Send a request to get access to restricted data in a record
In some cases the files in a dataset published in B2SHARE that you want to use for your own research is currently not publicly accessibe. In that case you can request access to the owner of the record by providing a message and your personal details in a request using the API. An automatic email will be sent to the person that owns and/or administers the record. In this example, access is requested for record `b43a0e6914e34de8bd19613bcdc0d364`.

```python
>>> header = {"Content-Type": 'application/json'}
>>> data = {"message": "I would like to have access to your record",
            "name": "John Smith",
            "affiliation": "Some University",
            "email": "j.smith@example.com",
            "address": "Example street",
            "city": "ExampleCity",
            "country": "ExampleCountry",
            "zipcode": "12345",
            "phone": "7364017452"
           }
>>> params = {"access_token": token}
```

The header is again included to indicate that the payload is in JSON format. Similarly to the request in the previous section, the `accessrequests` indicator is added to the URL, and the data structure is provided as a serialized string. The request is done through the POST method and looks as follows:

```python
>>> url = "https://trng-b2share.eudat.eu/api/records/b43a0e6914e34de8bd19613bcdc0d364/accessrequests"
>>> r = requests.get(url, params=params, data=json.dumps(data), headers=header)
```

On a successful request, the response looks as follows:

```python
>>> print(r)
<Response [200]>
>>> print(r.text)
{
  "message": "An email was sent to the record owner."
}
```

## Get the statistics of a record
To get an idea how many times the files in your record are downloaded, the special API endpoint `/api/stats` exists that provides this information. You need a POST method with the following structure provided as data, including the statistic and the file bucket identifier:

```python
>>> params = {'fileDownloads': {'params': {'bucket_id': 'b0377611-d5a4-4683-9781-b83edcb86324'}, 'stat': 'bucket-file-download-total'}}
>>> print(simplejson.dumps(payload, indent=4))
{
    "fileDownloads": {
        "stat": "bucket-file-download-total",
        "params": {
            "bucket_id": "b0377611-d5a4-4683-9781-b83edcb86324"
        }
    }
}
```

Please note the value for the `stat` field which indicates that a file download statistic is being requested for the record the file bucket belongs to. With the payload serialized and a header specifying the request content type the request looks as follows:

```python
>>> headers = {'Content-Type': 'application/json'}
>>> r = requests.post('https://trng-b2share.eudat.eu/api/stats', data=simplejson.dumps(payload), headers=headers)
>>> print(r)
<Response [200]>
```

The returned data looks as follows:

```python
>>> print(simplejson.dumps(r.json(), indent=4))
{
    "fileDownloads": {
        "key_type": "terms",
        "field": "file_key",
        "buckets": [
            {
                "value": 1.0,
                "key": "sequence.txt"
            }
        ],
        "type": "bucket"
    }
}
```

In the array as value for the `bucket` field, the `key` and `value` fields can be found which indicate the download count for each file contained in the file bucket.

Please note the following:
- If the download count of each file in a bucket is zero there will be no data in the response text.
- The statistics of a record are not updated in realtime. It might take 15 minutes or more before a change is shown.
- The statistics of a record are deduplicated. A file download will only be incremented a single time in case a user downloads the same file multiple times in a 10 seconds window.


## Delete a draft record
Sometimes a created draft record will not be used as a final publication and therefore it needs to be deleted. B2SHARE supports deletion of draft records by the owner of that record or the site administrator.

In order to delete a draft record, a header and your access token are required:

```python
>>> header = {"Content-Type": 'application/json'}
>>> params = {"access_token": token}
```

To make the request, the draft record identifier is required along with the DELETE request operation with the `/api/records/<record_id>/draft` endpoint in the URL. The request then looks as follows:

```python
>>> url = "https://trng-b2share.eudat.eu/api/records/b43a0e6914e34de8bd19613bcdc0d364/draft"
>>> r = requests.delete(url, params=params, headers=header)
```

On a successful request, the response code should be 204 while there is no response message:

```python
>>> print(r)
<Response [204]>
>>> print(r.text)

```

## Delete a published record
Deleting a published record works similar to deleting draft records. The only caveat is that this request can only be done by a site administrator, i.e. the token that is sent with the request must be of a user with this role.

To delete a published record, again a header and your access token are required and use the `/api/records/<record_id>` endpoint:

```python
>>> header = {"Content-Type": 'application/json'}
>>> params = {"access_token": token}
```

Again, the removal is accomplished using the DELETE request operation. With the record identifier the request then looks as follows:

```python
>>> url = "https://trng-b2share.eudat.eu/api/records/b43a0e6914e34de8bd19613bcdc0d364"
>>> r = requests.delete(url, params=params, headers=header)
```

On a successful request, the response code should be 204 while there is no response message:

```python
>>> print(r)
<Response [204]>
>>> print(r.text)

```

Please note that the equivalent draft record of the published record is also deleted when the published record is removed.
