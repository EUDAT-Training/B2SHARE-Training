# B2SHARE Configuration
After successfully [installing](05_Installation.md) the prerequisites and B2SHARE software package, your B2SHARE instance needs to configured. This includes setting the super administrator.

The information on this page is partially based on the [B2SHARE installation guide](https://github.com/EUDAT-B2SHARE/b2share/blob/evolution/INSTALL.rst) provided by the developers. The submodule covers the full configuration of B2SHARE and corresponding services:
- Setting up and configuration of connected containers services
- Starting and stopping its services
- Entering the Docker environment
- General usage the b2share tool
- Troubleshooting

### Prerequisites
Please make sure you have completed the previous submodules and your instance is successfully running.

## Configuration of connected container services
To get an overview of all containers currently running using Docker, run the following command:

```sh
$ docker-compose ps
          Name                         Command               State                                              Ports
----------------------------------------------------------------------------------------------------------------------------------------------------------------
dockerize_b2share_1         /eudat/b2share.sh                Up      0.0.0.0:32795->5000/tcp
dockerize_elasticsearch_1   /docker-entrypoint.sh elas ...   Up      0.0.0.0:32793->9200/tcp, 0.0.0.0:32792->9300/tcp
dockerize_mq_1              rabbitmq-server --hostname ...   Up      15671/tcp, 0.0.0.0:32789->15672/tcp, 25672/tcp, 4369/tcp, 5671/tcp, 0.0.0.0:32790->5672/tcp
dockerize_nginx_1           nginx -g daemon off;             Up      0.0.0.0:443->443/tcp, 0.0.0.0:80->80/tcp
dockerize_postgres_1        docker-entrypoint.sh postgres    Up      0.0.0.0:32794->5432/tcp
dockerize_redis_1           docker-entrypoint.sh redis ...   Up      0.0.0.0:32791->6379/tcp
```

This command gives an overview of the currently running containers, run command, state and their location in the system.

## Controlling services
You can easily stop the B2SHARE service by entering:

```sh
$ docker-compose down
```

To start the containers again, enter:

```sh
$ docker-compose up -d
```

If there are any complaints about missing environment variables, make sure they are known to the host system (see [Installation guide](04_Installation.md#set-environment-variables))

### Removing currently built containers
If you encounter any problems or broken containers, it might help to remove all containers and start over again:

```sh
$ docker-compose rm -a
```

Run the [build and run commands](04_Installation.md#building-and-running-b2share) again to get your B2SHARE instance up and running again.

## Entering the Docker container environment
If you need to configure anything within one of the Docker containers it is possible to enter each one of them using the following command:

```sh
$ docker exec -it <container_name> /bin/bash
```

where `container_name` is the name of the container you want to enter, e.g.: `dockerize_b2share_1`.

You will automatically be located in the `/eudat/b2share` directory:

```sh
$ pwd
/eudat/b2share
```

## Using the b2share tool
Once you have entered the B2SHARE container `dockerize_b2share_1`, you can use the `b2share` tool to directly interact with the Invenio back-end:

```
$ b2share
/usr/lib/python3.4/site-packages/dojson/contrib/to_marc21/model.py:22: UserWarning: MARC21 undo feature is experimental
  warnings.warn('MARC21 undo feature is experimental')
Usage: b2share [OPTIONS] COMMAND [ARGS]...

  Command Line Interface for Invenio.

Options:
  --help  Show this message and exit.

Commands:
  access       Account commands.
  alembic      Perform database migrations.
  assets       Web assets commands.
  b2records    B2SHARE Records commands.
  collect      Collect static files.
  communities  communities management commands.
  db           Database commands.
  demo         Demonstration commands.
  deposit      Deposit management commands.
  files        Files management commands.
  index        Management command for search indicies.
  instance     Instance commands.
  migrate      Migration commands.
  npm          Generate a package.json file.
  oai          OAI commands.
  pid          PID-Store management commands.
  records      Record management commands.
  roles        Role commands.
  run          Runs a development server.
  schemas      Schemas management commands.
  shell        Runs a shell in the app context.
  users        User commands.
```

As is visible, there is a Python warning for a experimental feature. This can be ignored.

To see a complete overview of all commands in the b2share tool, see [Appendix A. The b2share tool reference](A_b2share_Tool_Reference.md)



## Troubleshooting
