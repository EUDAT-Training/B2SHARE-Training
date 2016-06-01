# Getting you API token

As already mentioned, B2HARE HTTP REST API will be used for interacting with B2SHARE via external programs. Only authenticated users can use the API. Authentication is made by passing an `access token` in the request.

This `access token` can be retrieved using the B2SHARE service website. This guide will take you through the steps to obtain **access tokens** which are required to access the B2SHARE service programmatically. 

Please note that tokens are for private use only and not to be shared with other persons or institutions. Sharing them enables other people to alter your deposits on your behalf.

## Setup your machine and connection
Please make sure your machine has been properly set up to use Python and required packages. Follow [this](A_Setup_and_install.md) guide in order to do so.

This guide assumes you have successfully registered your account on B2SHARE using your institutional credentials or social ID through B2ACCESS.

## The account page
To create new access tokens for personal use, you need to register them on the account `Personal access token / requests` page of the [B2SHARE website](https://trng-b2share.eudat.eu). 

 - After logging in, navigate to your [account page](https://trng-b2share.eudat.eu/youraccount/display) by clicking on your name on the home page of B2SHARE.
 - Click on the wrench next to 'Account' to go to your [profile settings page](https://trng-b2share.eudat.eu/account/settings/profile). 
 - Select the bottom option in the left menu to go to the application and token [settings page](https://trng-b2share.eudat.eu/account/settings/applications). Here you can register new application and tokens to use within your own applications and scripts.

<img src="img/B2SHARE-applications.png" alt="B2SHARE account applications and tokens" text="B2SHARE account applications and tokens" style="width: 80%">

## API token generation
Click on the `New token` button to generate a new personal access token. Enter a name which easily identifies the purpose for this key. By clicking `Create`, a new access token is generated which is only shown at this time. Store it somewhere in order to use later, like in a file. In this training material it is assumed that the generated token is stored in a file called `token`.

<img src="img/B2SHARE-generate-token.png" alt="B2SHARE generate token" text="B2SHARE generate token">

Click 'Save' to store the access token on the server and make it usable in your applications.

**Note 1:** Please note that this is the only time the access token is visible, so copy it to a safe place.
**Note 2:** *It is not possible to programmatically register new or administer existing tokens. This can only be done through the [B2SHARE website](https://trng-b2share.eudat.eu).*

### Testing your token
Once you have generated your access token, it can be used and tested in your own applications. Launch a Python session and follow the steps below to check whether the token works.

#### Read the token from file
Assuming you have stored the access token in a file named `token.txt` and it is accessible from the current working directory, you can read it using the following commands in a Python session:
```python
>>> f = open(r'token.txt', 'r')
>>> token = f.read()
```

Test your reading by displaying the value of your access token:

```python
>>> print token
d4N8Ni7VOTfpQDIlUqTIcmYAjg...
```

#### Retrieve existing deposits
We can use the token to display some deposits from the B2SHARE repository. Without explaining the detailed workings, the following command, issues a request to get all records from the repository without doing verification of the source:

```python
>>> import requests
>>> r = requests.get('https://trng-b2share.eudat.eu/api/records', params={'access_token': token}, verify=False)
```

Most likely you will get a warning about insecure connections through HTTPS. You can ignore that for now.

To check whether the request succeeded, the `r` variable contains the HTTP response code:

```python
>>> print r
<Response [200]>
```
The request was successful.

#### Display a record

The response variable also contains the actual result text of the request in JSON format. In this case, the result is all the records from the repository. To extract the first record, do the following:

```python
>>> import json
>>> result = json.loads(r.text)
>>> records = result["records"]
```

Using the JSON package the first record can be properly displayed:

```python
>>> print json.dumps(records[0], indent=4)
{
    "files": [
        {
            "url": "https://trng-b2share.eudat.eu/record/1/files/c33a933c-8202-11e3-92a1-005056943408.zip?version=1", 
            "name": "c33a933c-8202-11e3-92a1-005056943408.zip", 
            "size": 549252
        }
    ], 
    "domain": "linguistics", 
    "uploaded_by": "stranak@ufal.mff.cuni.cz", 
    "description": "This is a small sample dataset from PDT 2.0. As such it can be released under a very permissive CC-BY license.", 
    "contributors": [], 
    "creator": [
        "Haji\u010d, Jan"
    ], 
    "checksum": "c5450f4822ee3ff6a6c8c0a400c8ca5294770fb115e55b7aa70c5b9d116a0043", 
    "title": "Prague Dependency Treebank 2.0 Sample Data", 
    "PID": "http://hdl.handle.net/11113/1986e7ae-8203-11e3-8cd7-14feb57d12b9", 
    "open_access": true, 
    "record_id": 1, 
    "version": "", 
    "contact_email": "", 
    "licence": "CC-BY 4.0", 
    "publication_date": "20-01-2014", 
    "keywords": [
        "treebank", 
        "sample"
    ], 
    "alternate_identifier": "", 
    "domain_metadata": {
        "quality": "release", 
        "region": "Czechia", 
        "project_name": "", 
        "ling_resource_type": [
            "treebank"
        ], 
        "language_code": "ces Czech"
    }, 
    "resource_type": []
}
```

In this example, we just retrieve a list of records. To retrieve a specific record in a similar manner, please follow the [next](00_Retrieve_existing_deposit.md) guide.