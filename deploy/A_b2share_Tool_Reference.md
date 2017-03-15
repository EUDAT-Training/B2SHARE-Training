# b2share Tool Reference
This reference guide lists all the possible commands and options for the b2share tool.

### Accessing the b2share tool
The b2share tool is available in the B2SHARE Docker container. Read the dedicated [section](08_Configuration.md#entering-the-docker-container-environment) in the [Configuration](08_Configuration.md) guide to learn how to access it.

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
  list        List all communities in this instances...
  set_schema
```

### Subcommand help
To see a help for the create subcommand, enter:

```sh
$ b2share communities create --help
/usr/lib/python3.4/site-packages/dojson/contrib/to_marc21/model.py:22: UserWarning: MARC21 undo feature is experimental
  warnings.warn('MARC21 undo feature is experimental')
Usage: b2share communities create [OPTIONS] NAME DESCRIPTION LOGO

  Create a community in the database. Name can be 255 characters long.
  Description is a text of maximally 1024 characters enclosed in
  parentheses. The logo parameter should be a valid path to a logo file
  relative to B2SHARE_UI_PATH/img/communities directory

Options:
  -v, --verbose
  --help         Show this message and exit.
```

## Main commands
The following table lists the available commands in the b2share tool:

Command | Description
------- | -----------
access | Set access for specific accounts; list, allow or deny specific actions, show assigned actions
alembic | Perform database migrations; show and create revisions, show logs
assets | Web assets commands; build, clean and watch bundles
b2records | B2SHARE Records commands
collect | Collect static files
communities | communities management commands
db | Database commands
demo | Demonstration commands
deposit | Deposit management commands
files | Files management commands
index | Management command for search indicies
instance | Instance commands
migrate | Migration commands
npm | Generate a package.json file
oai | OAI commands
pid | PID-Store management commands
records | Record management commands
roles | Role commands
run | Runs a development server
schemas | Schemas management commands
shell | Runs a shell in the app context
users | User commands
