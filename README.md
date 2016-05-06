# B2SHARE-Training
Training material for the EUDAT B2SHARE service.

# Example script 'example.py'
The examples below explain the basic usage of the B2SHARE service REST API. More information can be found on the REST API page. You can freely use the [training instance](https://trng-b2share.eudat.eu) of the B2SHARE service to test your applications. You need to register a new account using your institutional B2ACCESS credentials.

## Deposition

### STEP 0: Prepare your API application
In order to use the REST API of the B2SHARE service you need to create a new API key to access the service. You can do this by generating one on your personal account. Log in to the service, navigate to your account page, click on the socket wrench next to 'Account', click on 'Applications', followed by 'New token' next to 'Personal access tokens'. See for a step-by-step guide the link above.

The generated key needs to be stored in a file called `token` which is read every time one of the example functions is called.

### STEP 1: Create a new deposition
To create a new deposition use the
```python
create_deposition()
```
function. It will register a test deposition in the service, but will not any files yet. A temporary file is created on your local file system.

### STEP 2: Upload a new file into a deposition object
```python
add_file('filename')
```

### STEP 3: List the files uploaded into a deposition object
```python
list_files()
```

### STEP 4: Commit deposition
```python
commit_deposition()
```

## Other uses
Please note that these functional examples need an API key. See Step 0 in the section above.

### List a specific record
List a specific record registered in the service.
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
