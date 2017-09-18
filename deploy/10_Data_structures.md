# Data structures
In this guide, the various data structures used throughout the B2SHARE instance are explained and configured to your own requirements.

This guide covers:
- Record data structure definition
- Community data structure definition
- Metadata schema structure definition

### Prerequisites
Please make sure you have completed the previous submodules and your instance is successfully running.

## Data structures
There are several data structures used throughout the B2SHARE service. All data is stored in JSON format and follows specific [JSON Schema](http://json-schema.org/) specifications.

### Record data structure
Data from an [existing published record](https://trng-b2share.eudat.eu/api/records/47077e3c4b9f4852a40709e338ad4620) is accessible through the API on the training B2SHARE instance.

```python
{
  "created": 
  "files": 
  "id":
  "links":
  "metadata":
  "updated":
}
```

### Community data structure

### Metadata schema data structure
An example metadata schema can be found [here](https://github.com/EUDAT-B2SHARE/b2share/blob/master/b2share/modules/schemas/root_schemas/root_schema_v0.json).

```python
{
    "version": 
    "json_schema": {
        "$schema": 
        "type": 
        "properties": 
        "required":
        "additionalProperties":
        "b2share":
    }
}
```

B2SHARE presentation:

```python
{
    "presentation": {
        "major": [ "community", "titles", "descriptions", "creators", "open_access", "embargo_date", "license", "disciplines", "keywords", "contact_email" ],
        "minor": [ "contributors", "resource_types", "alternate_identifiers", "version", "publisher", "language"]
    }
}
```