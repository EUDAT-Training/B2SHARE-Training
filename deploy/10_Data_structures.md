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
Data from an [existing published record](https://trng-b2share.eudat.eu/api/records/47077e3c4b9f4852a40709e338ad4620) is accessible through the API on the (training) B2SHARE instance.

The root level keys are as follows:

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
Data from an [community](https://trng-b2share.eudat.eu/api/communities/e9b9792e-79fb-4b07-b6b4-b9c2bd06d095) is accessible through the API on the (training) B2SHARE instance.

The root level keys are as follows:

```python
{
  "created":
  "description":
  "id":
  "links":
  "logo":
  "name":
  "publication_workflow":
  "restricted_submission":
  "roles":
  "updated":
}
```

where `logo` refers to a relative path storing the logo picture of the community, `name` equals the community name, while `publication_workflow` and `restricted_submission` respectively set the community policies for depositing new records and whether non-community members can make deposits under this community.

The `roles` field defines the available roles for this community and has the following structure:

```python
"roles": {
    "<rolename>": {
      "description":
      "id":
      "name": "com:<identifier>:<rolename>"
    }
}
```

with `description` a description of the role, `id` a unique successive number maintained by B2SHARE and `name` a string consisting of a fixed prefix 'com' followed by a unique identifier and the rolename delimited by colons. There can be as many roles defined as needed, each with a unique name.

### Metadata schema data structure
An example metadata schema can be found [here](https://github.com/EUDAT-B2SHARE/b2share/blob/master/b2share/modules/schemas/root_schemas/root_schema_v0.json).

The root level keys are as follows:

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
