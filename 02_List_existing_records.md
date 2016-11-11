# List existing records
In this guide the retrieval of a list of existing records in paginated form is shown. Furthermore, the filtering of records for specific communities is explained.

### Setup your connection
Please make sure your machine has been properly set up to use Python and required packages. Follow [this](A_Setup_and_install.md) guide in order to do so.

This guide assumes you have successfully registered your account on the [B2SHARE website](https://trng-b2share.eudat.eu) using your institutional credentials or social ID through B2ACCESS. In addition, the loading of the token, importing Python packages and checking request responses will not be covered here.

## Retrieve a paginated list of records
As shown in the guide '[Getting your API token](00_Getting_your_API_token.md)' all existing records can easily be retrieved using a single request:

```python
>>> r = requests.get('https://trng-b2share.eudat.eu/api/records', params={'access_token': token}, verify=False)
```

To avoid retrieving all records, which potentially may take a long time, the request can be improved by adding pagination parameters.
For example, to retrieve records 21 to 40, add the page size and offset:

```python
>>> payload = {'page_size': 20,
               'page_offset': 1,
               'access_token': token
               }
>>> r = requests.get('https://trng-b2share.eudat.eu/api/records', params=payload, verify=False)
```

To check whether any records are actually retrieved, the JSON package can be used. Indeed, 20 records were retrieved and the first and last one have index 21 and 40:

```python
>>> result = json.loads(r.text)
>>> print len(result["records"])
20
>>> print result["records"][0]["record_id"]
21
>>> print result["records"][19]["record_id"]
40
```

Please note that the actual response text is very long and therefore not very usable yet since it cannot be interpreted as a data structure:

```python
>>> print type(r.text), len(r.text)
<type 'unicode'> 38520
```

### Community-specific records
If you solely want the records of a given community, say linguistics, this name of the community can be added to the request URL in order to get them.

```python
>>> payload = {'page_size': 20,
               'page_offset': 1,
               'access_token': token
               }
>>> r = requests.get('https://trng-b2share.eudat.eu/api/records/linguistics', params=payload, verify=False)
```

By repeating the processing with JSON, the number of results can be displayed:
```python
>>> result = json.loads(r.text)
>>> print len(result["records"])
1
```

Each record is identical in structure as in the other requests. If an empty community collection is requested, the response will be positive, but the results structure will be empty:
```python
>>> r = requests.get('https://trng-b2share.eudat.eu/api/records/bbmri', params=payload, verify=False)
>>> print r
<Response [200]>
>>> result = json.loads(r.text)
>>> print result["records"]
```

To see which communities are available in B2SGARE, follow the [dedicated guide](03_Communities.md#list-all-communities).