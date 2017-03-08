# Community integration
Now that your B2SHARE instance is ready for use, communities can be added in order to allow the upload of new records.

This guide covers:
- Listing existing communities
- Adding new communities
- Configuring and updating communities
- Adding roles to specific users
- Adding users to your community

## Prerequisites
Please make sure that you have following all previous submodules and that your B2SHARE instance is correctly running.

All commands below are using the [b2share tool](08_Configuration.md#Using-the-b2share-tool) after successfully [entering](08_Configuration.md#Entering-the-Docker-container-environment) the `dockerize_b2share_1` container.

### Listing existing communities
To see a list of the currently known communities run the following command:

```sh
$ b2share communities list
surfsara    3343bcab-a442-4dc5-a92e-f2ce1ff50b1a    SURFsara community    /img/communities/surfsara.png
```

It shows the name, identifier, description and logo location of each community. If there is no listing that means there are no communities configured yet.

## Add a new community
A new community can be added by a single command:

```sh
$ b2share communities create <community_name> "<description>" <logo>
```

where `community_name` is the name of your community, `description` is the text describing your community and `logo` is the path to an image containing the logo of your community. This path needs to be relative to `$B2SHARE_UI_PATH/img/communities`. All fields are mandatory.

If you don't have a logo image yet, set the `logo` argument to an existing one, e.g. `eudat.png`. To update your logo see the [Updating your community logo](#Updating-your-community-logo) section below.

## Configure your community
The name and description of an existing community can be edited by:

```sh
$ b2share communities edit <community_name> <option> <value>
```

where `community_name` is the name of your community, `option` is either '--name' or '--description' and `value` is the new value for the corresponding field.

## Setting the community metadata schema
Define a metadata schema for your community by preparing a JSON file which describes the fields of the metadata schema. The installation of B2SHARE provides several existing community JSON files that can be used as a starting point for your own community. Copy an existing one from `/eudat/b2share/demo/b2share_demo/data/communities/block_schemas/`, or create a new one with the following contents (including one metadata schema field specified):

```json
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "My Community Metadata Schema",
    "description": "This is the blueprint of the metadata block specific for My Community community",
    "type": "object",
    "properties": {
        "study_id": {
            "title": "Study ID",
            "description": "The unique ID or acronym for the study",
            "type": "string"
        }
    },
    "additionalProperties": false
}
```

To attach the schema to your community enter:

```sh
$ b2share communities set_schema <community_name> <community_metadata_file>
```

where `community_name` is the name of your community and `community_metadata_file` is the name of the JSON metadata schema file.

## Updating your community logo
Upload a logo into your Docker container or download one directly from the web using `wget` or a similar tool.

```sh
$ b2share communities edit <community_name> --logo <path>
```

Please note that the path needs to be relative to the `<B2SHARE_UI_PATH>/img/communities` directory. The `B2SHARE_UI_PATH` environment variable can be found by running:

```sh
$ echo $B2SHARE_UI_PATH
```

## Adding roles to specific users

## Adding users to your community
