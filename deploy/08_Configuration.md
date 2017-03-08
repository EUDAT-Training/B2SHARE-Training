# Configuration
After successfully [installing](05_Installation.md) the prerequisites and B2SHARE software package, your B2SHARE instance needs to configured.

The information on this page is based on the [B2SHARE installation guide](https://github.com/EUDAT-B2SHARE/b2share/blob/evolution/INSTALL.rst) provided by the developers. The submodule covers the full configuration of B2SHARE and corresponding services:
- Setting up and configuration of connected containers services
- Starting and stopping its services
- Entering the Docker environment
- Troubleshooting

## Prerequisites
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

If there are any complaints about missing environment variables, make sure they are known to the host system (see [Installation guide](04_Installation.md#Set-environment-variables))

### Removing currently built containers
If you encounter any problems or broken containers, it might help to remove all containers and start over again:

```sh
$ docker-compose rm -a
```

Run the [build and run commands](04_Installation.md#Building-and-running-B2SHARE) again to get your B2SHARE instance up and running again.
