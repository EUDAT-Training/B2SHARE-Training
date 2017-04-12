# Update all community metadata fields
In most cases all metadata fields of a community metadata schema need to be filled in upon submit. In this guide, the community metadata schema definition is processed to obtain all required and optional fields. A JSON patch is prepared that will update these fields based on input from a locally-stored metadata file.

This guide covers:
- Getting and analysing the community metadata schema definition
- Investigating the required field structure and contents
- Creating a structure with metadata values from file
- Two scenarios:
 - Using the structure to add metadata for new records
 - Creating a JSON patch that can modify the current record metadata
- Submitting the metadata using the corresponding required request method

### Community metadata schemas
For a more elaborate description of metadata schema definitions in B2SHARE, refer to the [Data Structures](../deploy/10_Data_strucutres.md) guide in the deploy module of this repository. For a general introduction of JSON Schemas, check out their [online book](https://spacetelescope.github.io/understanding-json-schema) which gives a quick general introduction.

## Getting the community metadata schema definition and structure
To get the latest version of the metadata schema definition of for example the EUDAT community, do the following:

```python
>>> r = requests.get('https://trng-b2share.eudat.eu/api/communities/e9b9792e-79fb-4b07-b6b4-b9c2bd06d095/schemas/last')
>>> print r
<Response [200]>
>>> print r.text
{
  "community": "e9b9792e-79fb-4b07-b6b4-b9c2bd06d095",
  "draft_json_schema": {
    "$ref": "https://trng-b2share.eudat.eu/api/communities/e9b9792e-79fb-4b07-b6b4-b9c2bd06d095/schemas/0#/json_schema",
    "$schema": "http://json-schema.org/draft-04/schema#"
  },
}
...
```

The response text contains a long listing of all required fields and their data types and structure. The high-level structure is shown as follows:

```python
>>> schema = json.loads(r.text)
>>> print schema.keys()
[u'version', u'links', u'json_schema', u'draft_json_schema', u'community']
```

The `json_schema` key contains the actual description and requirements of all metadata schema blocks. Blocks are groups of metadata fields. All blocks are required since they are contained as a list in the `allOf` substructure and there are no `anyOf` or `oneOf` structures:

```python
>>> print schema['json_schema'].keys()
[u'allOf']
>>> print len(schema['json_schema']['allOf'])
2
```

The list of this substructure contains two elements that both contain a schema block. In this case, the second block has no fields defined, so only the first block is processed.

### Investigate the block metadata fields
A block structure contains several keywords that give more information on the requirements for the metadata:

```python
>>> block = schema['json_schema']['allOf'][0]
>>> print block.keys()
[u'b2share', u'required', u'additionalProperties', u'$schema', u'type', u'properties']
```

To find all metadata fields that are defined in this block and can be used to add descriptive metadata, the keywords of the `properties` substructure are examined. All keywords that start with an underscore or dollar sign can be ignored. Therefore the following commands suffice:

```python
>>> fields = block["properties"]
>>> metadata_fields = {k: v for k,v in fields.items() if k[0].isalnum()}
>>> print metadata_fields.keys()
[u'embargo_date', u'contributors', u'community', u'titles', u'descriptions', u'keywords', u'open_access', u'alternate_identifiers', u'version', u'disciplines', u'publisher', u'contact_email', u'publication_date', u'community_specific', u'publication_state', u'resource_types', u'language', u'license', u'creators']
>>> print len(metadata_fields)
19
```

The required metadata fields of this metadata block are stored in the `required` structure:

```python
>>> print block["required"]
[u'community', u'titles', u'open_access', u'publication_state', u'community_specific']
>>> print len(block["required"])
5
```

For this block, 5 of 19 metadata fields must be filled in before the draft record can be submitted. The complete listing and properties of all metadata fields in this block can be found in the accompanying [JSON file](metadata/eudat-metadata.json).

To see the descriptions of each metadata field and learn what is expected to be provided for these fields, do the following:

```python
>>> for k,v in metadata_fields.items(): print "%s (%s): %s" % (v["title"], k, v["description"]) if "description" in v else ""
```
```
Publisher (publisher): The entity responsible for making the resource available, either a person, an organization, or a service.
Embargo Date (embargo_date): The date marking the end of the embargo period. The record will be marked as open access on the specified date at midnight. Please note that the record metadata is always publicly accessible, and only the data files can have private access.
License (license): Specify the license under which this data set is available to the users (e.g. GPL, Apache v2 or Commercial). Please use the License Selector for help and additional information.
Resource Type (resource_types): The type(s) of the resource.
Alternate identifiers (alternate_identifiers): Any kind of other reference such as a URN, URI or an ISBN number.
Contributors (contributors): The list of all other contributors. Please mention all persons that were relevant in the creation of the resource.
Publication State (publication_state): State of the publication workflow.
Open Access (open_access): Indicate whether the record's files are publicly accessible or not. In case of restricted access the uploaded files will only be accessible by the record's owner and the community administrators. Please note that the record's metadata is always publicly accessible.
Community (community): The community to which the record has been submitted.
Language (language): The primary language of the resource. Please use ISO_639-3 language codes.
Titles (titles): The title(s) of the uploaded resource, or a name by which the resource is known.
Contact Email (contact_email): Contact email information for this record.
Descriptions (descriptions): A more elaborate description of the resource. Focus on a content description that makes it easy for others to find, and to interpret its relevance.
Version (version): Denote the version of the resource.
Keywords (keywords): A list of keywords or key phrases describing the resource.
Publication Date (publication_date): The date when the data was or will be made publicly available (e.g. 1971-07-13)
Creators (creators): The full name of the creators. The personal name format should be: family, given (e.g.: Smith, John).
Disciplines (disciplines): The scientific disciplines linked with the resource.
```

### Investigate single metadata field structures
Each metadata field in a block has its own `description`, `title` and `type` keywords that uniquely identify the metadata field in the web interface. Depending on whether a field can have multiple values or has a more complex structure, additional keywords are available. For example, the 'embargo_date' metadata field can have only a single value formatted as a date, while the 'titles' metadata field can have multiple values, provided as an array of unique key-value pairs:

```python
>>> print json.dumps(fields["embargo_date"], indent=4)
{
    "title": "Embargo Date",
    "type": "string",
    "description": "The date marking the end of the embargo period. The record will be marked as open access on the specified date at midnight. Please note that the record metadata is always publicly accessible, and only the data files can have private access.",
    "format": "date-time"
}
```

Some fields are defined as an object (or substructure) containing different subfields with their own values. Not all subfields are required:

```python
>>> print json.dumps(fields["license"], indent=4)
{
    "description": "Specify the license under which this data set is available to the users (e.g. GPL, Apache v2 or Commercial). Please use the License Selector for help and additional information.",
    "title": "License",
    "required": [
        "license"
    ],
    "additionalProperties": false,
    "type": "object",
    "properties": {
        "license_uri": {
            "title": "URL",
            "type": "string",
            "format": "uri"
        },
        "license": {
            "type": "string"
        }
    }
}
```

In some cases the field is even more complex, as is shown in the following example for the 'descriptions' field:

```python
>>> print json.dumps(fields["descriptions"], indent=4)
{
    "uniqueItems": true,
    "items": {
        "additionalProperties": false,
        "required": [
            "description",
            "description_type"
        ],
        "type": "object",
        "properties": {
            "description": {
                "type": "string"
            },
            "description_type": {
                "enum": [
                    "Abstract",
                    "Methods",
                    "SeriesInformation",
                    "TableOfContents",
                    "TechnicalInfo",
                    "Other"
                ],
                "title": "Type"
            }
        }
    },
    "type": "array",
    "description": "A more elaborate description of the resource. Focus on a content description that makes it easy for others to find, and to interpret its relevance.",
    "title": "Descriptions"
}
```

Here the provided values must be an array of objects of which each object consists of two subfields: a `description` string and a `description_type` which can only have specific values defined in the `enum` substructure. Both fields are required, as is indicated by the `required` substructure.

The expected type of the value is defined in the `type` field of the field definition. To obtain a list all fields that only require a single value (string, boolean or number), do the following:

```python
>>> print [k for k,v in metadata_fields.items() if v["type"] in ["string", "boolean", "integer"]]
[u'publisher', u'embargo_date', u'publication_state', u'community', u'language', u'contact_email', u'version', u'publication_date']
```

Metadata fields that require an array of values:

```python
>>> print [k for k,v in metadata_fields.items() if v["type"] == "array"]
[u'resource_types', u'alternate_identifiers', u'contributors', u'titles', u'descriptions', u'keywords', u'creators', u'disciplines']
```

Finally, the metadata fields that must be structured as an object are:

```python
>>> print [k for k,v in metadata_fields.items() if v["type"] == "object"]
[u'community_specific', u'license']
```

Given these structures and lists, for each metadata field the right information can be provided upon making the PATCH request to the B2SHARE server.

## Provide metadata values by file
The values of metadata fields are often stored in separate files along with the actual research data. In this section, a comma-separated value (CSV) [file](metadata/eudat-metadata.csv) is used to get the values for each metadata field.

In the metadata file, the first column represents the metadata field names, the second the optional subfield name in that field, while the columns thereafter indicate the actual values, one or more for each field. Together with the community metadata schema definition a structure is generated that can be used to create a JSON patch, which can be uploaded along with the PATCH request to the B2SHARE service.

Run the test function in the Python [load.py](metadata/load.py) file to see what how the resulting metadata structure looks like. You are free to use this code in your own projects, but please note that there is no error checking at all, it solely serves for this example.

### Load the new metadata from file
Using the code from the example [Python load module](metadata/load.py), the new metadata is loaded from the CSV file and can be used to derive the required changes. For the code below, you need to run the interactive Python session from the metadata folder in this module, or change the work directory before running loading the module and running the code (as shown below):

```python
>>> import os
>>> os.chdir('metadata')
>>> import load
>>> metadata_new = load.getMetadata('eudat-metadata.csv', 'e9b9792e-79fb-4b07-b6b4-b9c2bd06d095')
>>> print json.dumps(metadata_new, indent=4)
{
    "publisher": "EUDAT",
    "embargo_date": "2017-09-01T17:00:00+01:00",
    "license": {
        "license_uri": "https://opensource.org/licenses/mit-license.php",
        "license": "MIT"
    },
    "resource_types": [
        {
            "resource_type_general": "Text",
            "resource_type": "Numbered text"
        }
    ],
    "alternate_identifiers": [
        {
            "alternate_identifier": "10.5072/b2share.b43a0e6914e34de8bd19613bcdc0d364",
            "alternate_identifier_type": "DOI"
        }
    ],
    "contributors": [
        {
            "contributor_name": "John Smith",
            "contributor_type": "ContactPerson"
        },
        {
            "contributor_name": "John Doe",
            "contributor_type": "DataManager"
        }
    ],
    "open_access": true,
    "community": "e9b9792e-79fb-4b07-b6b4-b9c2bd06d095",
    "language": "en_GB",
    "titles": [
        {
            "title": "My test upload"
        },
        {
            "title": "This is really my test upload"
        }
    ],
    "contact_email": "email@example.com",
    "descriptions": [
        {
            "description": "My first dataset ingested using the B2SHARE API",
            "description_type": "Abstract"
        },
        {
            "description": "First",
            "description_type": "SeriesInformation"
        }
    ],
    "version": "1",
    "keywords": [
        "test",
        "series",
        "numbers",
        "example"
    ],
    "publication_date": "2017-03-02",
    "creators": [
        {
            "creator_name": "Jane Smith"
        },
        {
            "creator_name": "Jane Doe"
        }
    ],
    "disciplines": [
        "Mathematics",
        "Number theory"
    ]
}
```

### Updating an existing record
In this section, the metadata of the existing published record `b43a0e6914e34de8bd19613bcdc0d364` is updated with the metadata of the CSV file. This record has been published under the EUDAT community and can therefore be updated using the EUDAT metadata schema definition that has been loaded in the previous sections.

#### Get the current metadata
As has been shown in the previous guides, the current record metadata is obtained by requesting the record from B2SHARE. Because the record will be edited, the draft version is requested using the designated endpoint in the URL. Please make sure you have your token loaded in the variable `token`:

```python
>>> recordid = 'b43a0e6914e34de8bd19613bcdc0d364'
>>> url = "https://trng-b2share.eudat.eu/api/records/" + recordid
>>> payload = {'access_token': token}
>>> r = requests.get(url, params=payload)
>>> result = json.loads(r.text)
```

The current record metadata looks as follows:

```python
>>> metadata = result["metadata"]
>>> print json.dumps(metadata, indent=4)
{
    "community_specific": {},
    "publication_state": "published",
    "open_access": true,
    "DOI": "http://doi.org/10.5072/b2share.b43a0e6914e34de8bd19613bcdc0d364",
    "language": "en_GB",
    "publisher": "EUDAT",
    "ePIC_PID": "http://hdl.handle.net/11304/ab379f3b-8ff2-41ff-a96b-a3a066cc820c",
    "community": "e9b9792e-79fb-4b07-b6b4-b9c2bd06d095",
    "titles": [
        {
            "title": "My test upload"
        }
    ],
    "contact_email": "email@example.com",
    "descriptions": [
        {
            "description": "My first dataset ingested using the B2SHARE API",
            "description_type": "Abstract"
        }
    ],
    "owners": [
        10
    ],
    "$schema": "https://trng-b2share.eudat.eu/api/communities/e9b9792e-79fb-4b07-b6b4-b9c2bd06d095/schemas/0#/draft_json_schema"
}
```

#### Prepare the JSON patch
To update the metadata a JSON patch needs to be prepared containing all changes in the metadata values. Together with the new and old metadata, the JSON patch is constructed as follows:

```python
>>> import jsonpatch
>>> patch = jsonpatch.make_patch(metadata, metadata_new)
>>> print patch
[{"path": "/community_specific", "op": "remove"}, {"path": "/publication_state", "op": "remove"}, {"path": "/DOI", "op": "remove"}, {"path": "/ePIC_PID", "op": "remove"}, {"path": "/titles/1", "value": {"title": "This is really my test upload"}, "op": "add"}, {"path": "/descriptions/1", "value": {"description": "First", "description_type": "SeriesInformation"}, "op": "add"}, {"path": "/owners", "op": "remove"}, {"path": "/$schema", "op": "remove"}, {"path": "/embargo_date", "value": "2017-09-01T17:00:00+01:00", "op": "add"}, {"path": "/license", "value": {"license_uri": "https://opensource.org/licenses/mit-license.php", "license": "MIT"}, "op": "add"}, {"path": "/resource_types", "value": [{"resource_type_general": "Text", "resource_type": "Numbered text"}], "op": "add"}, {"path": "/alternate_identifiers", "value": [{"alternate_identifier": "10.5072/b2share.b43a0e6914e34de8bd19613bcdc0d364", "alternate_identifier_type": "DOI"}], "op": "add"}, {"path": "/contributors", "value": [{"contributor_name": "John Smith", "contributor_type": "ContactPerson"}, {"contributor_name": "John Doe", "contributor_type": "DataManager"}], "op": "add"}, {"path": "/version", "value": "1", "op": "add"}, {"path": "/keywords", "value": ["test", "series", "numbers", "example"], "op": "add"}, {"path": "/publication_date", "value": "2017-03-02", "op": "add"}, {"path": "/creators", "value": [{"creator_name": "Jane Smith"}, {"creator_name": "Jane Doe"}], "op": "add"}, {"path": "/disciplines", "value": ["Mathematics", "Number theory"], "op": "add"}]
```

Any values of metadata fields that are added or changed are included in the patch. Values that do not change are not touched. Unfortunately, the patch now also contains several operations that will delete existing metadata field values that are not present in the new metadata values:

```python
>>> print filter(lambda x: x["op"] == "remove", patch)
[{u'path': u'/community_specific', u'op': u'remove'}, {u'path': u'/publication_state', u'op': u'remove'}, {u'path': u'/DOI', u'op': u'remove'}, {u'path': u'/ePIC_PID', u'op': u'remove'}, {u'path': u'/owners', u'op': u'remove'}, {u'path': u'/$schema', u'op': u'remove'}]
```

These operations therefore need to be removed from the patch, as the values are still needed for the descriptive and technical metadata:

```python
>>> patch_new = filter(lambda x: x["op"] != "remove", patch)
>>> print patch_new
[{u'path': u'/titles/1', u'value': {'title': 'This is really my test upload'}, u'op': u'add'}, {u'path': u'/descriptions/1', u'value': {'description': 'First', 'description_type': 'SeriesInformation'}, u'op': u'add'}, {u'path': u'/embargo_date', u'value': '2017-09-01T17:00:00+01:00', u'op': u'add'}, {u'path': u'/license', u'value': {'license_uri': 'https://opensource.org/licenses/mit-license.php', 'license': 'MIT'}, u'op': u'add'}, {u'path': u'/resource_types', u'value': [{'resource_type_general': 'Text', 'resource_type': 'Numbered text'}], u'op': u'add'}, {u'path': u'/alternate_identifiers', u'value': [{'alternate_identifier': '10.5072/b2share.b43a0e6914e34de8bd19613bcdc0d364', 'alternate_identifier_type': 'DOI'}], u'op': u'add'}, {u'path': u'/contributors', u'value': [{'contributor_name': 'John Smith', 'contributor_type': 'ContactPerson'}, {'contributor_name': 'John Doe', 'contributor_type': 'DataManager'}], u'op': u'add'}, {u'path': u'/version', u'value': '1', u'op': u'add'}, {u'path': u'/keywords', u'value': ['test', 'series', 'numbers', 'example'], u'op': u'add'}, {u'path': u'/publication_date', u'value': '2017-03-02', u'op': u'add'}, {u'path': u'/creators', u'value': [{'creator_name': 'Jane Smith'}, {'creator_name': 'Jane Doe'}], u'op': u'add'}, {u'path': u'/disciplines', u'value': ['Mathematics', 'Number theory'], u'op': u'add'}]
```

An alternative approach would be to filter the existing metadata fields for fields that will not be altered and then create the patch.

#### Update the record metadata
To update the record metadata, a serialized JSON patch is sent to the B2SHARE server in a PATCH request.

First, the request headers and payload need to be prepared:

```python
>>> header = {'Content-Type': 'application/json-patch+json'}
>>> payload = {'access_token': token}
```

After the request has been made, the new metadata can be shown:

```python
>>> r = requests.patch(url, data=json.dumps(patch_new), params=payload, headers=header)
>>> print r
<Response [200]>
>>> result = json.loads(r.text)
>>> print json.dumps(result, indent=4)
{
  "created": "2017-03-02T17:07:13.895604+00:00",
  "id": "b43a0e6914e34de8bd19613bcdc0d364",
  "links": {
    "files": "https://trng-b2share.eudat.eu/api/files/c1422a22-b8d4-42d6-9e94-1e5590294cb4",
    "self": "https://trng-b2share.eudat.eu/api/records/b43a0e6914e34de8bd19613bcdc0d364"
  },
  "metadata": {
    "$schema": "https://trng-b2share.eudat.eu/api/communities/e9b9792e-79fb-4b07-b6b4-b9c2bd06d095/schemas/0#/json_schema",
    "DOI": "http://doi.org/10.5072/b2share.b43a0e6914e34de8bd19613bcdc0d364",
    "alternate_identifiers": [
      {
        "alternate_identifier": "10.5072/b2share.b43a0e6914e34de8bd19613bcdc0d364",
        "alternate_identifier_type": "DOI"
      }
    ],
    "community": "e9b9792e-79fb-4b07-b6b4-b9c2bd06d095",
    "community_specific": {},
    "contact_email": "email@example.com",
    "contributors": [
      {
        "contributor_name": "John Smith",
        "contributor_type": "ContactPerson"
      },
      {
        "contributor_name": "John Doe",
        "contributor_type": "DataManager"
      }
    ],
    "creators": [
      {
        "creator_name": "Jane Smith"
      },
      {
        "creator_name": "Jane Doe"
      }
    ],
    "descriptions": [
      {
        "description": "My first dataset ingested using the B2SHARE API",
        "description_type": "Abstract"
      },
      {
        "description": "First",
        "description_type": "SeriesInformation"
      }
    ],
    "disciplines": [
      "Mathematics",
      "Number theory"
    ],
    "ePIC_PID": "http://hdl.handle.net/11304/ab379f3b-8ff2-41ff-a96b-a3a066cc820c",
    "embargo_date": "2017-09-01T17:00:00+01:00",
    "keywords": [
      "test",
      "series",
      "numbers",
      "example"
    ],
    "language": "en_GB",
    "license": {
      "license": "MIT",
      "license_uri": "https://opensource.org/licenses/mit-license.php"
    },
    "open_access": true,
    "owners": [
      10
    ],
    "publication_date": "2017-03-02",
    "publication_state": "published",
    "publisher": "EUDAT",
    "resource_types": [
      {
        "resource_type": "Numbered text",
        "resource_type_general": "Text"
      }
    ],
    "titles": [
      {
        "title": "My test uploads"
      },
      {
        "title": "This is really my test upload"
      }
    ],
    "version": "1"
  },
  "updated": "2017-04-12T14:00:36.096395+00:00"
}
```

The metadata has been successfully updated, as can be seen on the actual [landing page of the record](https://trng-b2share.eudat.eu/records/b43a0e6914e34de8bd19613bcdc0d364).

### Creating a new record
When creating new records, the metadata values structure can be directly sent to the B2SHARE server without using a patch.

Because a record needs to be deposited under a community, the EUDAT community ID is added and the title is replaced by a single new string:

```python
>>> metadata_new['titles'] = {'title': 'My second test upload'}
>>> metadata_new['community'] = "e9b9792e-79fb-4b07-b6b4-b9c2bd06d095"
>>> r = requests.post('https://trng-b2share.eudat.eu/api/records/', params={'access_token': token}, data=json.dumps(metadata_new), headers=header)
```

Adding files, additional metadata and finally published the record is shown in the [Create new record](05_Create_new_record.md) guide.
