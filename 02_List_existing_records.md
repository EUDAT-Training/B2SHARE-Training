# List existing records
In this guide the retrieval of a list of existing records in paginated form is shown. Furthermore, the filtering of records for specific communities is explained.

### Setup your connection
Please make sure your machine has been properly set up to use Python and required packages. Follow [this](A_Setup_and_install.md) guide in order to do so.

This guide assumes you have successfully registered your account on the [B2SHARE website](https://trng-b2share.eudat.eu) using your institutional credentials or social ID through B2ACCESS. In addition, the loading of the token, importing Python packages and checking request responses will not be covered here.

## Retrieve a list of records
As shown in the guide '[Getting your API token](00_Getting_your_API_token.md)', to get the first set of records from the B2SHARE service, the following request suffices:

```python
>>> r = requests.get('https://trng-b2share.eudat.eu/api/records', params={'access_token': token}, verify=False)
```

B2SHARE also returns the total number of records in the service:

```python
>>> result = json.loads(r.text)
>>> print result["hits"]["total"]
341
```

To get all records, which potentially may take a long time, the request can be altered by adding pagination parameters. In the following request, the page size and offset parameters define which records are returned. Increasing the size to a larger number and setting the page offset gives different results:

```python
>>> payload = {'size': 100,
               'page': 1,
               'access_token': token
               }
>>> r = requests.get('https://trng-b2share.eudat.eu/api/records', params=payload, verify=False)
```

To check whether any records are actually retrieved, the JSON package can be used. Indeed, 341 records were found, but only records 101 to 200.

```python
>>> result = json.loads(r.text)
>>> print result["hits"]["total"]
341
>>> print len(result["hits"]["hits"])
100
```

Please note that the actual response text is very long and therefore not very usable yet since it cannot be interpreted as a data structure:

```python
>>> print type(r.text), len(r.text)
<type 'unicode'> 657711
```

### Sorting your results


To see what communities are available and which records they have published in B2SHARE, follow the [Communities guide](03_Communities.md).