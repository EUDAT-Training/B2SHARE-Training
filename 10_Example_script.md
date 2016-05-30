# Example script
In this repository an example Python script file is included, called [example.py](example.py). You can use the functions defined in your own tools and applications.

The examples below explain the basic usage of the B2SHARE service REST API using these functions. More information can be found on the B2SHARE [REST API page](https://trng-b2share.eudat.eu/docs/b2share-rest-api). You can freely use the [training instance](https://trng-b2share.eudat.eu) of the B2SHARE service to test your applications.

## Setup your machine and connection
Please make sure your machine has been properly set up to use Python and required packages. Follow [this](A_Setup_and_install.md) guide in order to do so.

This guide assumes you have successfully registered your account on B2SHARE using your institutional credentials or social ID through B2ACCESS.

## General information
The example script uses a few additional packages to ease the handling of data in the script.

```python
import json
from urlparse import urljoin
```
The `json` package is used to parse and display JSON-formatted strings, while `urljoin` can construct full URLs based on separate strings. Please note that the latter package only works in Python 2.x. For later versions, use `urllib.parse` [instead](https://docs.python.org/2/library/urllib.html).

## Deposition of data sets
This section shortly explains how to create new deposits of data sets in B2SHARE.

### Step 0: Prepare your API application
Please follow the [Getting your API token](00_Getting_your_API_token.md) in order to get your API token. The generated token needs to be stored in a file called `token` which is read every time one of the example functions is called.

### Step 1: Create a new deposition
To create a new deposition use the
```python
create_deposition()
```
function. It will register a test deposition in the service, but does not containg any files or metadata yet. A temporary file is created on your local file system.

### Step 2: Add new files to a deposition
To add files to the deposition, use the following function:
```python
add_file('filename')
```
This function can be used multiple times in order to add multiple files.

### Step 3: List the files uploaded into a deposition object
To check which files are currentyl attached, use:
```python
list_files()
```

### Step 4: Commit deposition
To finalize the deposition into a new record, use the commit function:
```python
commit_deposition()
```
Currently, all metadata values are fixed.

## Other uses
Please note that these functional examples need an API key. See Step 0 in the section above.

### List a specific record
List a specific record registered in the service:
```python
list_specific_record('154')
```

### List all the records
List all registered records in the service instance:
```python
list_records()
```

List registered records in the service instance paginated:
```python
list_records_pagination(3, 10)
```
