# B2SHARE Administration
After successfully [installing](05_Installation.md) the prerequisites and B2SHARE software package and configuring it, your B2SHARE instance needs to administered. This includes setting the super administrator.

The information on this page is partially based on the [B2SHARE installation guide](https://github.com/EUDAT-B2SHARE/b2share/blob/evolution/INSTALL.rst) provided by the developers. The submodule covers the full configuration of B2SHARE and corresponding services:
- Starting and stopping its services
- Overview of running containers services
- Entering the Docker environment
- General usage of the b2share tool
- Troubleshooting

### Prerequisites
Please make sure you have completed the previous submodules and your instance is successfully running.

## Controlling services
You can easily stop the B2SHARE service by entering:

```sh
$ docker-compose down
```

This will show something similar to this:

```sh
Stopping dockerize_nginx_1_74bd49abc586         ... done
Stopping dockerize_b2share_1_86f511306d51       ... done
Stopping dockerize_elasticsearch_1_5f03dfc7159a ... done
Stopping dockerize_redis_1_e7d0b9f6afdf         ... done
Stopping dockerize_postgres_1_c71f97f3be2d      ... done
Stopping dockerize_mq_1_7eec59c0e21e            ... done
Removing dockerize_nginx_1_74bd49abc586         ... done
Removing dockerize_b2share_1_86f511306d51       ... done
Removing dockerize_elasticsearch_1_5f03dfc7159a ... done
Removing dockerize_redis_1_e7d0b9f6afdf         ... done
Removing dockerize_postgres_1_c71f97f3be2d      ... done
Removing dockerize_mq_1_7eec59c0e21e            ... done
Removing network dockerize_default
```

If successful, the service is down and no longer accessible.

To start the containers again, enter:

```sh
$ docker-compose up -d
```

If there are any complaints about missing environment variables, make sure they are known to the host system (see [Installation guide](04_Installation.md#set-environment-variables))

## Overview of running container services
To get an overview of all containers currently running using Docker, run the following command:

```sh
$ docker-compose ps
```

It will provide an output similar to this:

```sh
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

If any of the containers failed to start, the output for that container will be similar to the following:

```sh
dockerize_b2share_1_951516193d48         /eudat/b2share.sh                Exit 1
```

Check the logs to determine the cause of the early exit.

### Removing currently built containers
If you encounter any problems or broken containers, it might be helpful to remove all containers and start over again:

```sh
$ docker-compose rm
```

Run the [build and run commands](04_Installation.md#building-and-running-b2share) again to get your B2SHARE instance up and running again.

## Entering the Docker container environment
If you need to configure anything within one of the Docker containers it is possible to enter each one of them using the following command:

```sh
$ docker exec -it <container_name> /bin/bash
```

where `container_name` is the name of the container you want to enter, e.g.: `dockerize_b2share_1`. You can use tab completion for the container name.

You will automatically be located in the `/eudat/b2share` directory:

```sh
$ pwd
/eudat/b2share
```

### General inspection
If B2SHARE is not building properly or the web service cannot be accessed, first inspect the logs of the Docker containers:

```sh
$ sudo docker-compose logs -f b2share
```

Try if you can find any reported problems which might impact the performance of the system.

## The b2share tool
Once you have entered the B2SHARE container `dockerize_b2share_1`, you can use the `b2share` tool to directly interact with the Invenio back-end.

To see a complete overview of all commands in the b2share tool, see [Appendix A. The b2share tool reference](A_b2share_Tool_Reference.md)
