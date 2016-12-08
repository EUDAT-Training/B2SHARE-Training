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
>>> r = requests.get('https://vm0045.kaj.pouta.csc.fi/api/records/e116249df8dc41b19e3f4a74ed014f35', params={'access_token': token}, verify=False)
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
  "created": "2016-11-16T10:55:54.688312+00:00",
  "files": [
    {
      "bucket": "7c484701-f0f1-4d5e-952b-083b89ebec97",
      "checksum": "md5:747d977beac19b97909b61120b17a6c6",
      "ePIC_PID": "http://hdl.handle.net/11304/883afb20-0f1f-41c2-a5f2-6dfbc35f7f18",
      "key": "200Mpc_radio_2Jy_z=0.0_hb.fits",
      "size": 57602880,
      "version_id": "e57863d0-a30e-4c93-a085-5118417e9acb"
    },
    {
      "bucket": "7c484701-f0f1-4d5e-952b-083b89ebec97",
      "checksum": "md5:d67b0d07770fc6fc6b4d817ca72c0a15",
      "ePIC_PID": "http://hdl.handle.net/11304/2f0bec42-ebfd-4023-a922-b5f28439182f",
      "key": "200Mpc_radio_2Jy_z=0.5_hb.fits",
      "size": 57602880,
      "version_id": "348c8ea0-3f17-4413-adfd-d22d25f14714"
    },
    {
      "bucket": "7c484701-f0f1-4d5e-952b-083b89ebec97",
      "checksum": "md5:5e9d41cbf13cfec097b5a46ba3099df5",
      "ePIC_PID": "http://hdl.handle.net/11304/adc9cb5b-c2d0-496d-9f70-fcde640a31de",
      "key": "200Mpc_radio_2Jy_z=1.0_hb.fits",
      "size": 57602880,
      "version_id": "a8f5f49a-18b9-448b-98e6-d01c8ead4009"
    }
  ],
  "id": "e116249df8dc41b19e3f4a74ed014f35",
  "links": {
    "files": "https://vm0045.kaj.pouta.csc.fi/api/files/7c484701-f0f1-4d5e-952b-083b89ebec97",
    "self": "https://vm0045.kaj.pouta.csc.fi/api/records/e116249df8dc41b19e3f4a74ed014f35"
  },
  "metadata": {
    "$schema": "https://vm0045.kaj.pouta.csc.fi/api/communities/e9b9792e-79fb-4b07-b6b4-b9c2bd06d095/schemas/0#/json_schema",
    "DOI": "10.5072/b2share.fecb0192-65d0-433a-8187-8cd254fb2c3d",
    "alternate_identifier": "http://hdl.handle.net/11304/31bd2e7a-deda-11e4-ac7e-860aa0063d1f",
    "community": "e9b9792e-79fb-4b07-b6b4-b9c2bd06d095",
    "contact_email": "franco.vazza@hs.uni-hamburg.de",
    "contributors": [],
    "description": "Simulated radio emission at 120 MHz from a projected comoving volume of (200Mpc)^3 simulated with 1200^3 cells, at z=1.0, z=0.5 and z=0.0. Each map has units log10[J/arcsec^2]. The pixel size is 166kpc at z=0, 111kpc at z=0.5 and 83kpc at z=1.0\nEach .fits file is 1200x1200x10. The 10 frames contain=0-4 emission models (from Vazza et al. 2015 A&A); 5-9 spectral indices of radio emission (where 5->0, 6->1 etc). 0=injection of electrons as in Hoeft & Bruggen 2007, no shock reacceleration. 1=high-amplification model & shock injection and re-acceleration; 2=as 1, but low amplification model for the magnetic field; 3=as 1, plus CR-driven amplification of magnetic field; 4=shock injection and re-acceleration, magnetic field from the original MHD simulation. From 5 o 9 we have the spectral index of the radio emission,alfa, where I(freq) \\propto freq^-alfa. Details in http://adsabs.harvard.edu/abs/2015arXiv150308983V\n\n",
    "ePIC_PID": "http://hdl.handle.net/11304/052906f2-1fb5-45be-a558-cc690cb1e333",
    "keywords": [
      "ENZO",
      "MHD simulations",
      "radio"
    ],
    "open_access": true,
    "owners": [
      8
    ],
    "publication_state": "published",
    "resource_type": [],
    "title": "Simulated radio emission for 200Mpc"
  },
  "updated": "2016-11-16T10:55:54.688323+00:00"
}
```

Although the response text is nicely indented, the data can't be mapped through indexes yet.

### Process your record

To improve the usability of the response text, use the JSON package. This package turns the reponse text in a easily processable data structure called a dictionary:

```python
>>> import json
>>> result = json.loads(r.text)
>>> print json.dumps(result["metadata"], indent=4)
{
    "publication_state": "published",
    "open_access": true,
    "DOI": "10.5072/b2share.fecb0192-65d0-433a-8187-8cd254fb2c3d",
    "description": "Simulated radio emission at 120 MHz from a projected comoving volume of (200Mpc)^3 simulated with 1200^3 cells, at z=1.0, z=0.5 and z=0.0. Each map has units log10[J/arcsec^2]. The pixel size is 166kpc at z=0, 111kpc at z=0.5 and 83kpc at z=1.0\nEach .fits file is 1200x1200x10. The 10 frames contain=0-4 emission models (from Vazza et al. 2015 A&A); 5-9 spectral indices of radio emission (where 5->0, 6->1 etc). 0=injection of electrons as in Hoeft & Bruggen 2007, no shock reacceleration. 1=high-amplification model & shock injection and re-acceleration; 2=as 1, but low amplification model for the magnetic field; 3=as 1, plus CR-driven amplification of magnetic field; 4=shock injection and re-acceleration, magnetic field from the original MHD simulation. From 5 o 9 we have the spectral index of the radio emission,alfa, where I(freq) \\propto freq^-alfa. Details in http://adsabs.harvard.edu/abs/2015arXiv150308983V\n\n",
    "contributors": [],
    "title": "Simulated radio emission for 200Mpc",
    "owners": [
        8
    ],
    "ePIC_PID": "http://hdl.handle.net/11304/052906f2-1fb5-45be-a558-cc690cb1e333",
    "community": "e9b9792e-79fb-4b07-b6b4-b9c2bd06d095",
    "contact_email": "franco.vazza@hs.uni-hamburg.de",
    "keywords": [
        "ENZO",
        "MHD simulations",
        "radio"
    ],
    "alternate_identifier": "http://hdl.handle.net/11304/31bd2e7a-deda-11e4-ac7e-860aa0063d1f",
    "$schema": "https://vm0045.kaj.pouta.csc.fi/api/communities/e9b9792e-79fb-4b07-b6b4-b9c2bd06d095/schemas/0#/json_schema",
    "resource_type": []
}
```

Our request was successful and we now have all the information to process the record, its metadata and its files. The data is exactly the same as the data displayed on the [landing page](https://trng-b2share.eudat.eu/record/1) of the record.

#### Getting specific metadata values

To display specific information from the metadata, simply add the field name as an index to the `result` variable. For example, to solely display the id, do the following:

```python
>>> print result["id"]
e116249df8dc41b19e3f4a74ed014f35
```

Similarly, the file name of the first file can be displayed using an additional numerical zero-based index on the `files` key followed by the `key` index:

```python
>>> print result["files"][0]["key"]
200Mpc_radio_2Jy_z=0.0_hb.fits
```

### Downloading files from a record

In many cases, the files in a record are needed to allow further processing of the data set. A simple loop allows to get all files and store them at a specific location. Since all files are publically accessible, no authentication is required by access token as used earlier.

To avoid overwriting any existing files, a specific download folder is created in the current working directory using the Python package `os`:
```python
>>> import os
>>> os.mkdir('download')
```

Using the `urllib` package, files can be directly downloaded by URL:

```python

>>> import urllib
>>> for f in result["files"]:
...     with open("download/" + f["key"], 'wb') as fout:
...             rf = requests.get("https://vm0045.kaj.pouta.csc.fi/api/files/%s/%s" % (f["bucket"], f["key"]), verify=False)
...             fout.write(rf.content)
...
(u'download/c33a933c-8202-11e3-92a1-005056943408.zip', <httplib.HTTPMessage instance at 0x10ca86098>)
```

Again, you might get warning about unverified requests through HTTPS, these can be ignored.

Since no further Python errors are returned or exceptions raised, the download has been successful and the files are available on the system.
