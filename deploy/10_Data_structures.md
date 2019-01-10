# Data structures
This reference guide lists the various data structures used within the B2SHARE software package.

This guide covers:
- Record data structure definition
- File bucket data structure definition
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

where `files` contains the metadata for files and `metadata` the actual metadata describing the data object, including the DOI and EPIC persistent identifiers. The `created` and `updated` fields provide the dates when the object was created and updated, while `id` represents the object identifier. The `links` structure gives URLs for the object itself, the version and/or the file bucket.

### File bucket data structure definition
Data from a [file bucket](https://trng-b2share.eudat.eu/api/files/2686d997-87e2-457f-996e-436bb55a84af), in this case the file bucket of the above record, is accessible through the API on the (training) B2SHARE instance.

The root level keys are as follows:

```python
{
  "contents":
  "created":
  "locked":
  "updated":
  "id":
  "size":
  "quota_size":
  "links":
  "max_file_size":
}
```

Here, the `created`, `updated`, `links` and `id` field represent similar values as in the record data structure. The `contents` field contains an array of structures, one for each file in the file bucket. The `locked` field indicates whether the file bucket can be changed (for file buckets of published records this is always true), while the `size`, `quote_size` and `max_file_size` give the total data size, quota size and maximum allowed data size for the bucket respectively.

A structure in the `contents` field for a file has the following structure:

```python
{
  "updated":
  "size":
  "mimetype":
  "delete_marker":
  "version_id":
  "key":
  "created":
  "links":
  "checksum":
  "is_head":
}
```

Again, the `created`, `updated` and `links` fields are equivalent to those in the record data structure. The `size`, `mimetype`, `checksum` and `key` give the size, mimetype, checksum and name of the file respectively, while the `version_id` contains a unique identifier for that version of the file. The `is_head` and `delete_marker` boolean fields indicate whether this file is the original and whether it is marked for deletion for during a cleanup round.

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

In addition to the equivalent fields as for the record data strucuture, the `logo` field refers to a relative path storing the logo picture of the community, `name` equals the community name, while `publication_workflow` and `restricted_submission` respectively set the community policies for depositing new records and whether non-community members can make deposits under this community.

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

The `version` field is a unique (successive) number for the different versions of the schema. The `json_schema` is the actual schema with most importantly the `properties` field giving the properties and a description of each metadata field in the schema.

The `b2share` field provides information on the presentation of the schema on the B2SHARE deposit workflow form:

```python
{
    "presentation": {
        "major": [ "community", "titles", "descriptions", "creators", "open_access", "embargo_date", "license", "disciplines", "keywords", "contact_email" ],
        "minor": [ "contributors", "resource_types", "alternate_identifiers", "version", "publisher", "language"]
    }
}
```

where the fields in the `major` structure are shown on top of the form and the `minor` fields are shown more below under the 'Show more details' toggle. You can define any key name in the presentation object, though they will be added to the `major` key upon display of the schema.
