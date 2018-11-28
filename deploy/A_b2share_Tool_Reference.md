# b2share Tool Reference
This reference guide lists all the possible commands and options for the b2share tool.

### Accessing the b2share tool
The `b2share` tool is available in the B2SHARE Docker container. Read the dedicated [section](08_Configuration.md#entering-the-docker-container-environment) in the [Configuration](08_Configuration.md) guide to learn how to access it.

### General syntax
The general syntax for the `b2share` tool is:

```sh
$ b2share [options] command [args]
```

where `options` are one or more of the options possibly specific for the given `command`. Any of the `args` are specific values that correspond to the value of the `command` given.

### General help
Enter one of the following commands to see all available commands:

```sh
$ b2share
```

```sh
$ b2share --help
```

### Command-specific help
Additional help regarding specific commands can be requested by adding the command argument followed by the `--help` option. This holds for any of the commands and the options thereafter, e.g. to see the listing of the communities help, enter:

```sh
$ b2share communities --help
Usage: b2share communities [OPTIONS] COMMAND [ARGS]...

  communities management commands.

Options:
  --help  Show this message and exit.

Commands:
  create      Create a community in the database.
  edit        Edit data of the specified community.
  list        List all communities in this instances'...
  set_schema
```

where the `options`, `command` and `args` arguments are the same as described for the general syntax.

### Subcommand help
To see a help for the `create` subcommand of the `communities` command, enter:

```sh
$ b2share communities create --help
Usage: b2share communities create [OPTIONS] NAME DESCRIPTION LOGO

  Create a community in the database. Name can be 255 characters long.
  Description is a text of maximally 1024 characters enclosed in
  parentheses. The logo parameter should be a valid path to a logo file
  relative to B2SHARE_UI_PATH/img/communities directory

Options:
  -v, --verbose
  --help         Show this message and exit.
```

## Main commands and subcommands
The following table lists the available commands in the `b2share` tool. Click on a link to see the options and/or subcommands for that command.

| Command | Description |
| ------- | ----------- |
| [alembic](#alembic) | Perform database migrations |
| [assets](#assets) | Web assets commands |
| [b2records](#b2records) | B2SHARE Records commands |
| [collect](#collect) | Collect static files |
| [communities](#communities) | communities management commands |
| [demo](#demo) | Demonstration commands |
| [deposit](#deposit) | Deposit management commands |
| [files](#files) | Files management commands |
| [index](#index) | Manage search indices |
| [instance](#instance) | Instance commands |
| [migrate](#migrate) | Migration commands. WARNING csc only |
| [npm](#npm) | Generate a package.json file |
| [oai](#oai) | OAI commands |
| [pid](#pid) | PID-Store management commands |
| [queues](#queues) | Manage events queue |
| [records](#records) | Record management commands |
| [roles](#roles) | Role commands |
| [run](#run) | Runs a local development server for the Flask application. This local server is recommended for development purposes only but it can also be used for simple intranet deployments.  By default it will not support any sort of concurrency at all to simplify debugging.  This can be changed with the --with-threads option which will enable basic multithreading. The reloader and debugger are by default enabled if the debug flag of Flask is enabled and disabled otherwise |
| [schemas](#schemas) | Schemas management commands |
| [shell](#shell) | Runs an interactive Python shell in the context of a given Flask application. The application will populate the default namespace of this shell according to it's configuration. This is useful for executing small snippets of management code without having to manually configuring the application |
| [upgrade](#upgrade) | B2SHARE upgrade commands |
| [users](#users) | User commands |

#### alembic
Perform database migrations.

| Subcommand | Description |
| ---------- | ----------- |
| branches | Show branch points |
| current | Show current revision |
| downgrade | Run downgrade migrations |
| heads | Show latest revisions |
| log | Show revision log |
| merge | Create merge revision |
| mkdir | Make migration directory |
| revision | Create new migration |
| show | Show the given revisions |
| stamp | Set current revision |
| upgrade | Run upgrade migrations |

#### assets
Web assets commands.

| Subcommand | Description |
| ---------- | ----------- |
| build | Build bundles |
| clean | Clean bundles |
| watch | Watch bundles for file changes |

#### b2records
B2SHARE Records commands.

| Subcommand | Description |
| ---------- | ----------- |
| check_and_update_handle_records | Checks that PIDs of records and files have... |
| check_dois | Checks that DOIs of records in the current... |
| check_handles | Allocate handles for a record and its files,... |
| update_expired_embargoes | Updates all records with expired embargoes to... |

#### collect
Collect static files.

| Option | Description |
| ---------- | ----------- |
| -v, --verbose | Verbose output |

#### communities
communities management commands.

| Subcommand | Description |
| ---------- | ----------- |
| create | Create a community in the database |
| edit | Edit data of the specified community |
| list | List all communities in this instances'... |
| set_schema

#### db
Database commands.

| Subcommand | Description |
| ---------- | ----------- |
| create | Create tables |
| destroy | Drop database |
| drop | Drop tables |
| init | Create database |

#### demo
Demonstration commands.

| Subcommand | Description |
| ---------- | ----------- |
| load_config | Copy the demo configuration to the... |
| load_data | Load demonstration data |

#### deposit
Deposit management commands.

| Subcommand | Description |
| ---------- | ----------- |
| create | Create new deposit |
| discard | Discard selected deposits |
| edit | Make selected deposits editable |
| publish | Publish selected deposits |
| schema | Create deposit schema from an existing... |

#### files
Files management commands.

| Subcommand | Description |
| ---------- | ----------- |
| add-location | Add a file storage location |
| list-locations | List all file storage locations |
| set-default-location | Change the default file storage location |

#### index
Manage search indices.

| Subcommand | Description |
| ---------- | ----------- |
| create | Create new index |
| delete | Delete index by its name |
| destroy | Destroy all indexes |
| init | Initialize registered aliases and mappings |
| put | Index input data |
| queue | Manage indexing queue |
| reindex | Reindex all records |
| run | Run bulk record indexing |

#### instance
Instance commands.

| Subcommand | Description |
| ---------- | ----------- |
| create | Create a new Invenio instance from template |
| entrypoints | List defined entry points |

#### migrate
Migration commands. WARNING csc only.

| Subcommand | Description |
| ---------- | ----------- |
| add_missing_alternate_identifiers | Add missing alternate identifiers from v1... |
| check_pids | Checks and optionally fixes ePIC PIDs from... |
| diff_sites
| extract_alternate_identifiers | Extracting alternate identifiers from v1... |
| import_v1_data
| swap_pids | Fix the invalid creation of new ePIC_PIDs for... |

#### npm
Generate a package.json file.

| Option | Description |
| ------ | ----------- |
| -i, --package-json FILENAME | Base input file `FILENAME` |
| -o, --output-file FILENAME | Write package.json to output file `FILENAME` |
| -p, --pinned-file FILENAME | Pinned versions package file `FILENAME` |

#### oai
OAI commands.

| Subcommand | Description |
| ---------- | ----------- |
| update_records_set | Check that each record oai entry has a set |
| update_sets | Check that each community has a corresponding... |

#### pid
PID-Store management commands.

| Subcommand | Description |
| ---------- | ----------- |
| assign | Assign persistent identifier |
| create | Create new persistent identifier |
| dereference | Show linked persistent identifier(s) |
| get | Get an object behind persistent identifier |
| unassign | Unassign persistent identifier |

#### queues
Manage events queue.

| Subcommand | Description |
| ---------- | ----------- |
| declare | Initialize the given queues |
| delete | Delete the given queues |
| list | List configured queues |
| purge | Purge the given queues |

#### records
Record management commands.

| Subcommand | Description |
| ---------- | ----------- |
| create | Create new bibliographic record(s) |
| delete | Delete bibliographic record(s) |
| patch | Patch existing bibliographic record |

#### roles
Role commands.

| Subcommand | Description |
| ---------- | ----------- |
| add | Add user to role |
| create | Create a role |
| remove | Remove user from role |

#### run
Runs a local development server for the Flask application. This local server is recommended for development purposes only but it can also be used for simple intranet deployments.

By default it will not support any sort of concurrency at all to simplify debugging.  This can be changed with the `--with-threads` option which will enable basic multithreading.

The reloader and debugger are by default enabled if the debug flag of Flask is enabled and disabled otherwise.

| Option | Description |
| ------ | ----------- |
| -h, --host TEXT | The interface to bind to |
| -p, --port INTEGER | The port to bind to |
| --reload / --no-reload | Enable or disable the reloader.  By default the reloader is active if debug is enabled |
| --debugger / --no-debugger | Enable or disable the debugger.  By default the debugger is active if debug is enabled |
| --eager-loading / --lazy-loader | Enable or disable eager loading.  By default eager loading is enabled if the reloader is disabled |
| --with-threads / --without-threads | Enable or disable multithreading |

#### schemas
Schemas management commands.

| Subcommand | Description |
| ---------- | ----------- |
| block_schema_add | Adds a block schema to the database |
| block_schema_create_version | Assign a json-schema file conforming to the... |
| block_schema_edit
| block_schema_list | Lists all block schemas for this b2share... |
| block_schema_list_versions | show the version number and release date of... |
| block_schema_version_generate_json | print json_schema of a particular block... |
| community_schema_list_block_schema_versions | Show the block schema versions in the... |
| init | CLI command loading Root Schema files in the... |

#### shell
Runs an interactive Python shell in the context of a given Flask application. The application will populate the default namespace of this shell according to it's configuration. This is useful for executing small snippets of management code without having to manually configuring the application.

#### upgrade
B2SHARE upgrade commands.

| Subcommand | Description |
| ---------- | ----------- |
| run | Upgrade the database to the last version and... |

#### users
User commands.

| Subcommand | Description |
| ---------- | ----------- |
| activate | Activate a user |
| create | Create a user |
| deactivate | Deactivate a user |
