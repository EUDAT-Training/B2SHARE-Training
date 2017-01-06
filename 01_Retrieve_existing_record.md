# Retrieve record details
In this guide the retrieval of details of a specific record in the B2SHARE service via the GET HTTP request is shown. In addition, retrieval of specific metadata values (checksum, files) and downloading files from a record is explained.

Using the information of a record, the corresponding files, metadata and other information can be used to automate data processing and transfer complete deposits to other services.

### Setup your connection
Please make sure your machine has been properly set up to use Python and required packages. Follow [this](A_Setup_and_install.md) guide in order to do so.

This guide assumes you have successfully registered your account on the [B2SHARE website](https://trng-b2share.eudat.eu) using your institutional credentials or social ID through B2ACCESS.

### Get details of a specific record

To retrieve a specific record, the `record_id` of that record is required and needs to be sent through the API. The data used in this GET request are:

 - URL path: `/api/records/<record_id>`: The basic url extended with the `record_id` value
 - Required parameters: `access_token`

As already described, the value of the access token is read from the `token.txt` file in Python as follows:

```python
>>> f = open(r'token.txt', 'r')
>>> token = f.read()
```
Now that you have the token value, prepare your HTTP GET request with the `requests` library:

```python
>>> import requests
>>> r = requests.get('https://trng-b2share.eudat.eu/api/records/41ccbfb505e641de8a75cc0b0f3818e2', params={'access_token': token}, verify=False)
```

Most likely you will get a warning (as shown below) about insecure connections through HTTPS. You can ignore this.

```python
/usr/lib/python2.7/dist-packages/urllib3/connectionpool.py:732: InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.org/en/latest/security.html (This warning will only appear once by default.)
  InsecureRequestWarning)
```

To verify whether the request succeeded and see the result, print the variable `r` and the response text:
```python
>>> print r
<Response [200]>
>>> print r.text
{
  "created": "2016-12-21T14:19:42.919114+00:00",
  "files": [
    {
      "bucket": "b0bd6602-b02b-4475-917d-a2898cd6d7d7",
      "checksum": "md5:d6eb32081c822ed572b70567826d9d9d",
      "ePIC_PID": "http://hdl.handle.net/11304/5764cfdd-483b-41f5-b3ca-45d5fc4e35e7",
      "key": "test-file.txt",
      "size": 13,
      "version_id": "027ec8d0-eb50-4840-beb6-4a9a7f3f1cd4"
    }
  ],
  "id": "41ccbfb505e641de8a75cc0b0f3818e2",
  "links": {
    "files": "https://trng-b2share.eudat.eu/api/files/b0bd6602-b02b-4475-917d-a2898cd6d7d7",
    "self": "https://trng-b2share.eudat.eu/api/records/41ccbfb505e641de8a75cc0b0f3818e2"
  },
  "metadata": {
    "$schema": "https://trng-b2share.eudat.eu/api/communities/99916f6f-9a2c-4feb-a342-6552ac7f1529/schemas/0#/json_schema",
    "community": "99916f6f-9a2c-4feb-a342-6552ac7f1529",
    "community_specific": {
      "362e6f81-68fb-4d71-9496-34ca00e59769": {
        "categories_of_data_collected": [
          "Imaging data"
        ],
        "material_type": [
          "Serum"
        ],
        "sex": [
          ...
        ],
        "study_design": [
          "Twin-study"
        ],
        "study_name": "my study"
      }
    },
    "descriptions": [
      {
        "description": "my table of content",
        "description_type": "TableOfContents"
      }
    ],
    "ePIC_PID": "http://hdl.handle.net/11304/d1b5384d-6ca6-4e80-9170-309e49a3e03b",
    "open_access": true,
    "owners": [
      7
    ],
    "publication_state": "published",
    "titles": [
      {
        "title": "test_nharraud_BBMRI"
      }
    ]
  },
  "updated": "2016-12-21T14:19:42.919123+00:00"
}
```

Although the response text is nicely indented, the response text is always a string and therefore the data can't be mapped through dictionary indexes yet.

### Process your record

To improve the usability of the response text, use the JSON package to transform the data. This package turns the reponse text in a easily processable data structure called a dictionary:

```python
>>> import json
>>> result = json.loads(r.text)
```

Now the metadata of the record can be directly printed using the `metadata` key for the dictionary `result`. Don't forget the `indent=4` argument and value as otherwise the output will be in serialized form:
```
>>> print json.dumps(result["metadata"], indent=4)
{
    "community_specific": {
        "362e6f81-68fb-4d71-9496-34ca00e59769": {
            "study_design": [
                "Twin-study"
            ],
            "categories_of_data_collected": [
                "Imaging data"
            ],
            "material_type": [
                "Serum"
            ],
            "study_name": "my study",
            "sex": [
              ...
            ]
        }
    },
    "publication_state": "published",
    "open_access": true,
    "ePIC_PID": "http://hdl.handle.net/11304/d1b5384d-6ca6-4e80-9170-309e49a3e03b",
    "community": "99916f6f-9a2c-4feb-a342-6552ac7f1529",
    "titles": [
        {
            "title": "test_nharraud_BBMRI"
        }
    ],
    "descriptions": [
        {
            "description": "my table of content",
            "description_type": "TableOfContents"
        }
    ],
    "owners": [
        7
    ],
    "$schema": "https://trng-b2share.eudat.eu/api/communities/99916f6f-9a2c-4feb-a342-6552ac7f1529/schemas/0#/json_schema"
}
```

Our request was successful and we now have all the information to process the record, its metadata and its files. The data is exactly the same as the data displayed on the [landing page](https://trng-b2share.eudat.eu/records/41ccbfb505e641de8a75cc0b0f3818e2) of the record.

#### Getting specific metadata values

To display specific information from the metadata, simply add the field name as an index to the `result` variable. For example, to solely display the `id`, do the following:

```python
>>> print result["id"]
41ccbfb505e641de8a75cc0b0f3818e2
```

To list the available files in a record:

```python
>>> print json.dumps(result["files"], indent=4)
[
    {
        "checksum": "md5:d6eb32081c822ed572b70567826d9d9d",
        "bucket": "b0bd6602-b02b-4475-917d-a2898cd6d7d7",
        "ePIC_PID": "http://hdl.handle.net/11304/5764cfdd-483b-41f5-b3ca-45d5fc4e35e7",
        "version_id": "027ec8d0-eb50-4840-beb6-4a9a7f3f1cd4",
        "key": "test-file.txt",
        "size": 13
    }
]
```

The response contains the identifiers `ePIC_PID` and `version_id` which uniquely identify this file. The `bucket` field is used to retrieve the file for downloading, while the `checksum` is the MD5 hash of the file contents.

Similarly, the file name of the first file can be displayed using an additional numerical zero-based index on the `files` key followed by the `key` index:

```python
>>> print result["files"][0]["key"]
test-file.txt
```

### Downloading files from a record

In many cases, the files in a record are needed to allow further processing of the data set. A simple loop allows to get all files and store them at a specific location. Since all files are publically accessible, no access token for authentication is required as in the previous sections.

To avoid overwriting any existing files, a specific download folder is created in the current working directory using the Python package `os`:
```python
>>> import os
>>> os.mkdir('download')
```

Using the `urllib` package, files can be directly downloaded per file URL. Files are downloaded through the API using the following URL:
```
https://trng-b2share.eudat.eu/api/files/<FILE_BUCKET_ID>/<FILE_KEY>
```

Using the information from the previous section, a simple `for` loop downloads all files from the record and stores them under their original name:

```python
>>> import urllib
>>> for f in result["files"]:
...     with open("download/" + f["key"], 'wb') as fout:
...             rf = requests.get("https://trng-b2share.eudat.eu/api/files/%s/%s" % (f["bucket"], f["key"]), verify=False)
...             fout.write(rf.content)
...
```

Again, you might get warning about unverified requests through HTTPS, these can be ignored.

A single file was successfully downloaded:
```
>>> print rf
<Response [200]>
```

Since no further Python errors are returned or exceptions raised, the download has been successful and the files are available on the system.

#### Check file integrity

In order to check that the contents of the file haven't changed, the checksum can be regenerated using the `md5` package and compared to the checksum given by the metadata:

```python
>>> import md5
>>> fd = open('download/test-file.txt', 'r')
>>> d = fd.read()
>>> print md5.md5(dt).hexdigest()
d6eb32081c822ed572b70567826d9d9d
>>> print result["files"][0]["checksum"]
md5:d6eb32081c822ed572b70567826d9d9d
```

They are the same! Please note that B2SHARE adds a prefix to the checksum to indicate which checksum algorithm was used to generate the hash.

### Troubleshooting
When working with remote servers, information retrieval by making requests might not always be succeed. To check whether the request has been successful, always check the reponse code. The most commonly occuring codes are listed in the [HTTP reponse codes](B_Request_and_Metadata_Reference_Guide.md) table.
