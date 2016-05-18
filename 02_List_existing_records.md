# List existing records


### Setup your connection
Please make sure your machine has been properly set up to use Python and required packages. Follow [this](A_Setup_and_install.md) guide in order to do so.

This guide assumes you have successfully registered your account on the [B2SHARE website](https://trng-b2share.eudat.eu) using your institutional credentials or social ID through B2ACCESS. In addition, the loading of the token, importing Python packages and checking request responses will not be covered here.

### Retrieve a paginated listing
As shown in the submodule '[Getting your API token](00_Getting_your_API_token.md)' all existing records can easily be retrieved using a single request:

```python
>>> r = requests.get('https://trng-b2share.eudat.eu/api/records', params={'access_token': token}, verify=False)
```

To avoid retrieving all records, which potentially may take a long time, the request can be improved by adding pagination parameters. For example, to retrieve records 21 to 40, this can be indicated by adding the page size and offset:
```python
>>> payload = {'page_size': 20,
               'page_offset': 1,
               'access_token': token
               }
>>> r = requests.get('https://trng-b2share.eudat.eu/api/records', params=payload, verify=False)
```

To check whether we actually retrieved these records, the JSON package can be used again. Indeed, 20 records were retrieved and the first and last one have index 21 and 40:
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
>>> print len(result)
38520
```

