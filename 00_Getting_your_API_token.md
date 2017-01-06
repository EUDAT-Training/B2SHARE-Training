# Getting you API token

This guide will take you through the steps to obtain access tokens on the B2SHARE website. API or access tokens are required to access the B2SHARE service programmatically through the REST API.

The B2HARE HTTP REST API can be used for interaction with B2SHARE via external services or applications. Only authenticated users can do API requests. User authentication is done by passing an `access_token` parameter along with the request. This `access_oken` can be retrieved by generating one on the B2SHARE service website.

Please note that access tokens are for private use only and not to be shared with other persons or institutions. Sharing them enables other people to alter your data on your behalf.

## Setup your machine and connection
Please make sure your machine has been properly set up to use Python and required packages. Follow [this](A_Setup_and_install.md) guide in order to do so.

This guide assumes you have successfully registered your account on B2SHARE using your institutional credentials or social ID through B2ACCESS.

## The account page
To create new access tokens for personal use, you need to register them on the account `Personal access token / requests` page of the [B2SHARE website](https://trng-b2share.eudat.eu).

 - After logging in, navigate to your [account page](https://trng-b2share.eudat.eu/youraccount/display) by clicking on your name on the home page of B2SHARE.
 - Click on the wrench next to 'Account' to go to your [profile settings page](https://trng-b2share.eudat.eu/account/settings/profile).
 - Select the bottom 'Applications' option in the left menu to go to the application and token [settings page](https://trng-b2share.eudat.eu/account/settings/applications). Here you can register new application and tokens to use within your own applications and scripts.

<img src="img/B2SHARE-applications.png" alt="B2SHARE account applications and tokens" text="B2SHARE account applications and tokens" style="width: 80%">

## API token generation
Click on the `New token` button to generate a new personal access token. Enter a name which easily identifies the purpose for this key. By clicking `Create`, a new access token is generated which is only shown at this time. Store it somewhere in order to use later, like in a file. In this training material it is assumed that the generated token is stored in a file called `token.txt`.

<img src="img/B2SHARE-generate-token.png" alt="B2SHARE generate token" text="B2SHARE generate token">

Click 'Save' to store the access token on the server and make it usable in your applications.

**Note 1:** Please note that this is the only time the access token is visible, so copy it to a safe place.

**Note 2:** It is not possible to programmatically register new or administer existing tokens. This can only be done through the [B2SHARE website](https://trng-b2share.eudat.eu).

## Testing your token
Once you have generated your access token, it can be used and tested with your own applications. Launch a Python session and follow the steps below to verify whether the token works.

#### Read the token from file
Assuming you have stored the access token in a file named `token.txt` and it is accessible from the current working directory, you can read it using the following commands in a Python session:
```python
>>> f = open(r'token.txt', 'r')
>>> token = f.read().strip()
```

Note: The strip command here removes any training new line characters that may be added when you save the token to a file.

Test your reading by displaying the value of your access token:

```python
>>> print token
d4N8Ni7VOTfpQDIlUqTIcmYAjg...
```

#### Retrieve existing records
We can use the token to display some records from the B2SHARE repository. Without explaining the detailed workings, the following command issues a request to get all records from the repository without doing verification of the source:

```python
>>> import requests
>>> r = requests.get('https://vm0045.kaj.pouta.csc.fi/api/records', params={'access_token': token}, verify=False)
```

Most likely you will get a warning about insecure connections through HTTPS. You can ignore this.

To check whether the request succeeded, the `r` variable contains the HTTP response code:

```python
>>> print r
<Response [200]>
>>> print r.status_code
200
```
The request was successful.

#### Display a record

The response variable also contains the actual result text of the request in JSON format. In this case, the result is all the records from the repository. To extract the first record, do the following:

```python
>>> import json
>>> result = json.loads(r.text)
```

Although no maximum number of results is specified, B2SHARE will only return the first 10 results even though the total number of results is known:

```python
>>> print result["hits"]["total"]
341
>>> print len(result["hits"]["hits"])
10
```

To display a single record:

```python
>>> records = result["hits"]["hits"]
>>> print records[0]
{u'files': [{u'checksum': u'md5:c8afdb36c52cf4727836669019e69222', u'bucket': u'f7128c66-9b38-4ab9-a45d-14bffe55a496', u'version_id': u'f37fc7c7-c578-40f2-9024-bcbb05bfe347', u'key': u'myfile', u'size': 9}], u'updated': u'2016-11-16T10:23:23.426598+00:00', u'links': {u'files': u'https://vm0045.kaj.pouta.csc.fi/api/files/f7128c66-9b38-4ab9-a45d-14bffe55a496', u'self': u'https://vm0045.kaj.pouta.csc.fi/api/records/a1c2ef96a1e446fa9bd7a2a46d2242d4'}, u'created': u'2016-11-16T10:23:23.426590+00:00', u'id': u'a1c2ef96a1e446fa9bd7a2a46d2242d4', u'metadata': {u'community_specific': {u'362e6f81-68fb-4d71-9496-34ca00e59769': {u'material_type': [u'Other'], u'study_design': [u'Other'], u'principal_investigator': u'Amilcar Flores', u'study_description': u'REST mediates androgen receptor actions on gene repression and predicts early recurrence of prostate cancer', u'categories_of_data_collected': [u'Biological samples'], u'disease': u'C61', u'sex': [u'Male'], u'study_id': u'REST', u'study_name': u'REST'}}, u'publication_state': u'published', u'open_access': True, u'description': u'REST mediates androgen receptor actions on gene repression and predicts early recurrence of prostate cancer', u'title': u'REST paper 2014', u'owners': [1], u'community': u'99916f6f-9a2c-4feb-a342-6552ac7f1529', u'contact_email': u'x@example.com', u'keywords': [u'prostate cancer', u'REST', u'TFBS', u'ChiP-seq'], u'$schema': u'https://vm0045.kaj.pouta.csc.fi/api/communities/99916f6f-9a2c-4feb-a342-6552ac7f1529/schemas/0#/json_schema', u'resource_type': [u'Text']}}
```

Using the JSON package this record can be displayed properly:

```python
>>> print json.dumps(records[0], indent=4)
{
    "files": [
        {
            "checksum": "md5:c8afdb36c52cf4727836669019e69222",
            "bucket": "f7128c66-9b38-4ab9-a45d-14bffe55a496",
            "version_id": "f37fc7c7-c578-40f2-9024-bcbb05bfe347",
            "key": "myfile",
            "size": 9
        }
    ],
    "updated": "2016-11-16T10:23:23.426598+00:00",
    "links": {
        "files": "https://vm0045.kaj.pouta.csc.fi/api/files/f7128c66-9b38-4ab9-a45d-14bffe55a496",
        "self": "https://vm0045.kaj.pouta.csc.fi/api/records/a1c2ef96a1e446fa9bd7a2a46d2242d4"
    },
    "created": "2016-11-16T10:23:23.426590+00:00",
    "id": "a1c2ef96a1e446fa9bd7a2a46d2242d4",
    "metadata": {
        "community_specific": {
            "362e6f81-68fb-4d71-9496-34ca00e59769": {
                "material_type": [
                    "Other"
                ],
                "study_design": [
                    "Other"
                ],
                "principal_investigator": "Amilcar Flores",
                "study_description": "REST mediates androgen receptor actions on gene repression and predicts early recurrence of prostate cancer",
                "categories_of_data_collected": [
                    "Biological samples"
                ],
                "disease": "C61",
                "sex": [
                    "Male"
                ],
                "study_id": "REST",
                "study_name": "REST"
            }
        },
        "publication_state": "published",
        "open_access": true,
        "description": "REST mediates androgen receptor actions on gene repression and predicts early recurrence of prostate cancer",
        "title": "REST paper 2014",
        "owners": [
            1
        ],
        "community": "99916f6f-9a2c-4feb-a342-6552ac7f1529",
        "contact_email": "x@example.com",
        "keywords": [
            "prostate cancer",
            "REST",
            "TFBS",
            "ChiP-seq"
        ],
        "$schema": "https://vm0045.kaj.pouta.csc.fi/api/communities/99916f6f-9a2c-4feb-a342-6552ac7f1529/schemas/0#/json_schema",
        "resource_type": [
            "Text"
        ]
    }
}
```

In this example, we just retrieve a list of records. To retrieve a specific record in a similar manner, please follow the [next](01_Retrieve_existing_record.md) guide.
