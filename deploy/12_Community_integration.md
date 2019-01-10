# Community integration
Now that your B2SHARE instance is ready for use, communities can be added in order to allow the upload of new records.

This guide covers:
- Listing existing communities
- Adding new communities
- Configuring and updating communities
- Setting the community metadata schema
- Adding roles to specific users
- Adding users to your community

### Prerequisites
Please make sure that you have following all previous submodules and that your B2SHARE instance is correctly running.

All commands below are using the [b2share tool](A_b2share_Tool_Reference.md#general-syntax) after successfully [entering](08_Configuration.md#entering-the-docker-container-environment) the B2SHARE Docker container.

### After care
When new communities are added or existing ones are updated regarding community name and description, it is necessary to synchronize the list of communities with the OAI-PMH declared sets used for metadata harvesting by external metadata services like [B2FIND](https://b2find.eudat.eu).

After your community is finalized, use the following command:

```sh
$ b2share oai update_sets
```

## Listing existing communities
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

where `community_name` is the name of your community, `description` is the text describing your community and `logo` is the path to an image containing the logo of your community. All fields are mandatory.

The image path needs to be relative to `$B2SHARE_UI_PATH/img/communities`, so a single file name of an image that resides in the `/eudat/b2share/webui/app/img/communities` folder in your B2SHARE Docker container.

If you don't have a logo image yet, set the `logo` argument to an existing one, e.g. `eudat.png`. To update your logo see the [Updating your community logo](#updating-your-community-logo) section below.

## Configure your community
The name and description of an existing community can be edited by:

```sh
$ b2share communities edit <community_name> <option> <value>
```

where `community_name` is the name of your community, `option` is either '--name' or '--description' and `value` is the new value for the corresponding field.

### Setting the community metadata schema
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
    "required": ["study_id"],
    "additionalProperties": false
}
```

To attach the schema to your community enter:

```sh
$ b2share communities set_schema <community_name> <community_metadata_file>
```

where `community_name` is the name of your community and `community_metadata_file` is the name of the JSON metadata schema file.

If you do not want to add any communitiy-specific fields, you still need to create a block schema defining no fields:

```json
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "My Community Metadata Schema",
    "description": "This is the blueprint of the metadata block specific for My Community community",
    "type": "object",
    "properties": {},
    "additionalProperties": false
}
```

Make sure to omit the `required` field in the data. Add the block schema as described above.

### Updating your community logo
Upload a logo into your Docker container or download one directly from the web using `wget` or a similar tool.

```sh
$ b2share communities edit <community_name> --logo <path>
```

Please note that the path needs to be relative to the `<B2SHARE_UI_PATH>/img/communities` directory. The `B2SHARE_UI_PATH` environment variable can be found by running:

```sh
$ echo $B2SHARE_UI_PATH
```

Of course, you can fill in the variable directly.

## Adding roles to specific users
Each B2SHARE record is published under a community. A community is administered by a user and therefore the community administrator has certain special rights, for example to edit a published record's metadata and to add members to the community. Community members have the privilege to publish record as part of the community.

See for more general information on user role administration the [User management](09_User_management.md) guide.

### Adding a community administrator
In order to set users that have administrator privileges, first the community identifier `COMMUNITY_ID` needs to be determined. You can do this by [listing the communities](https://YOUR_B2SHARE/api/communities) through the B2SHARE REST API, find the community ID and run the following command:

```sh
$ b2share roles add <email_address> <role_name>
Role "<invenio_accounts.models.Role object at 0x7f9c9dc27e80>" added to user "User <id=1, email=email_address>" successfully.
```

where `role_name` is a combination of a prefix, `COMMUNITY_ID` (digits only) and the role type, for example `com:3343bcaba4424dc5a92ef2ce1ff50b1a:admin`. The argument `email_address` is the email address of the user you want to give administrator privileges.

You can also directly find the role name in the API listing of communities under `roles`:

```json
    ...
    "roles": {
      "admin": {
        "description": "Admin role of the community \"surfsara\"",
        "id": 1,
        "name": "com:3343bcaba4424dc5a92ef2ce1ff50b1a:admin"
      },
      "member": {
        "description": "Member role of the community \"surfsara\"",
        "id": 2,
        "name": "com:3343bcaba4424dc5a92ef2ce1ff50b1a:member"
      }
    }
    ...
```

The member role is also shown here, which is used in the next section.

### Adding members to your community
Similarly you can add members to a community which then can publish under the community and select the community during record creation. Use the same command as in the previous section, but change the role type in the `role_name` argument to 'member':

```sh
$ b2share roles add <email_address> com:3343bcaba4424dc5a92ef2ce1ff50b1a:member
Role "<invenio_accounts.models.Role object at 0x7f9c9dc27e80>" added to user "User <id=1, email=email_address>" successfully.
```

### Removing roles
To remove a role from a specific user, use its email address and the role name:

```sh
$ b2share roles remove <email_address> <role_name>
Role "<invenio_accounts.models.Role object at 0x7f224a3fd5f8>" removed from user "User <id=1, email=email_address>" successfully.
```
