# Metadata schemas
This guide explores the concept of metadata and metadata schemas in B2SHARE.

It covers:
- Metadata schema structure
- Metadata schema management
- Root schema management
- Metadata schema versioning

### Prerequisites
Please make sure you have completed the previous submodules and your instance is successfully running.

All commands below are using the [b2share tool](A_b2share_Tool_Reference.md#general-syntax) after successfully [entering](08_Configuration.md#entering-the-docker-container-environment) the B2SHARE Docker container.

## Metadata schema structure
In B2SHARE the concept of a metadata schema is the bundling of one or more metadata block schemas that contain definitions for one or more metadata fields. Each metadata field can be used to annotate a given record and its data according to specific type and formatting rules.

By default, a metadata schema contains the root schema block that defines the basic metadata fields based on the DataCite metadata schema definition. Every record in B2SHARE always adheres to this default schema, and optionally to the added block schemas specified by a community. The EUDAT community in B2SHARE only contains this default root schema block.

Communities can define additional metadata fields bundled in a metadata schema block. The community definition refers to a specific version of this block once it has been added to the community.

## Metadata schema management
Using the [b2share tool](A_b2share_Tool_Reference.md) of your B2SHARE instance you can manage the metadata schemas in your system.

### Listing existing metadata schemas
The different metadata schemas are equivalent to the communities they are tied to. Therefore, to see the existing metadata schemas, the different communities can be shown:

```sh
$ b2share communities list
```

### Listing all known metadata schema blocks
B2SHARE tracks every block schema and their versions. To get a list of all currently known block schemas, use the `block_schema_list` command:

```sh
$ b2share schemas block_schema_list
```

This will output something similar to this:

```
BLOCK SCHEMA
         ID             NAME        MAINTAINER  DEPRECATED  #VERSIONS
3a1f1dcf-d78a-4d56-a9e4-f5b00c1b93ae    TEST           TEST           False       6
```

It shows the identifier, schema and community name and whether the block is deprecated and the number of versions of that block.

### Listing all versions of a given metadata schema block
You can list all the versions of a given block schema using the same command, but with subcommand `block_schema_list_versions` followed by the identifier of the block schema.

Entering command

```sh
$ b2share schemas block_schema_list_versions 3a1f1dcf-d78a-4d56-a9e4-f5b00c1b93ae
```

outputs:

```sh
BLOCK SCHEMA VERSIONS FOR community <community-name>, block schema <community-name>
Version no. Release date
0   2018-11-28 16:38:07.877972
1   2018-11-29 09:27:42.458207
2   2018-11-29 09:50:21.304344
3   2018-11-29 09:51:02.559771
4   2018-11-29 09:56:23.529564
5   2018-11-29 09:57:22.425867
```

The existing versions are indicated with the release data (date of creation of that version).

### Listing a community's current block schema version
To see which version of a block schema is currently used for a community, use the `community_schema_list_block_schema_versions` subcommand with the name of the community:

```sh
$ b2share schemas community_schema_list_block_schema_versions <community-name>
```

The output will look as follows:

```sh
The following block schema versions are listed for community
        <community-name>, community schema version latest 5
Block schema: 3a1f1dcf-d78a-4d56-a9e4-f5b00c1b93ae, version url: https://<FQDN>/api/schemas/3a1f1dcf-d78a-4d56-a9e4-f5b00c1b93ae/versions/5#/json_schema
```

The last line divulges the currently used version, in this case 5.

## Root schema management
By default, the code repository of B2SHARE provides a single root schema (version 0) that will be loaded after setting up the service using the provided scripts or by running the following command in the B2SHARE docker container:

```
$ b2share schemas init
```

If you have added newer versions next to the one provided, they will be loaded as well, provided that they are compatible with the previous versions of the root schema. See also the next section.

### Adding a new root schema version
To add a new version of your root schema, duplicate the latest version of all existing root schema files in the [root schemas folder](https://github.com/EUDAT-B2SHARE/b2share/tree/master/b2share/modules/schemas/root_schemas) in the B2SHARE code repository.

All metadata fields of a newer version of the root schema must be compatible with the previous version, i.e. at least the type and internal field name must be the same for every field. Any other information (descriptions, enumerations, required fields and presentation) can be adapted as needed.

Run the following command to add your new version:

```
$ b2share schemas init
```

**Further implications**

Please be aware that any new root schema version will not be automatically used by existing communities and/or records. Therefore if you add a new root schema version, you need to update the exisitng communities. Existing records do not need to be changed, but they will use the root schema version at the time when they were created.

#### Upgrading existing communities
For communities, please update the used root schema version in the database. Log in to your database, connect to the `invenio` database and list the community table:

```sql
select * from b2share_community_schema_version;
```

The `root_schema` column indicates the used root schema version, which is `0` by default. To upgrade a community to a newer root schema version, simply change the value in this column, e.g. for root schema version `1` for community with identifier `4ba7c0fd-1435-4313-9c13-4d888d60321a`:

```sql
update b2share_community_schema_version set root_schema=1 where community='4ba7c0fd-1435-4313-9c13-4d888d60321a';
```

If you now load the landing page of that community, you will see the root schema fields have been updated. Any newly created record will be annotated using the new root schema version.
