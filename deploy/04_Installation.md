# Installation
This module will take you through the installation of the required package and software in order to deploy your own B2SHARE instance.

The information on this page is based on the [B2SHARE installation guide](https://github.com/EUDAT-B2SHARE/b2share/blob/evolution/INSTALL.rst) provided by the developers. It covers:

- Installing prerequisites
- Configuring B2ACCESS
- Installing tools and Docker
- Configuring environment variables

## Things to note
Installing B2SHARE comes with responsibility and as with every web service, security is very important. Therefore never install B2SHARE as user root, but instead create a separate user that is allowed to run the B2SHARE service. Log in as this user before you start installing the software.

## Supported platforms
Currently the following platforms are supported:

- Ubuntu 14.04+
- CentOS 6.7+

In the following guides it is assumed that B2SHARE is installed on Ubuntu. Any Ubuntu-specific commands should be translatable to other platforms without any complications. Make sure you are familiar with the package management tools of your OS of choice.

## Prerequisites
The following tools need to be installed:

- Git
- curl
- Docker Community Edition (CE)
- Docker Engine
- Docker Compose

Make sure your platform is fully up-to-date:

```sh
$ sudo apt-get update && sudo apt-get upgrade
```

## Configuring B2ACCESS
Before you can install B2SHARE, B2ACCESS needs to be configured. B2ACCESS is the only service that needs to be set up before you can proceed with installing B2SHARE. Please refer to the [services configuration guide for B2ACCESS](06_Services_configuration.md#Configuring+B2ACCESS) to learn how to do this.

## Install tools
The basic tools are installed by running the following command:

```sh
$ sudo apt-get install git curl
```

### Install Docker
To install Docker with Docker Engine, please follow the following guide installing Docker Community Edition (CE) for [Ubuntu](https://docs.docker.com/engine/installation/linux/ubuntu/) or [CentOS](https://docs.docker.com/engine/installation/linux/centos/). Guides for other platforms are provided on the general [installation overview](https://docs.docker.com/engine/installation/) page.

Please read the guides carefully as many steps are involved, including adding Docker's own package repository. After setting this up, run `apt-get update` so that the Docker packages can be found.

To check whether you have successfully installed Docker run:

```sh
$ sudo docker run hello-world
```

#### Running Docker as a non-root user
To successfully run Docker as a non-root user, the user you are using must be added to the `docker` Linux group.

First, create the group `docker`:

```sh
$ sudo groupadd docker
```

Add your user to the group:

```sh
$ sudo usermod -aG docker <user>
```

where `user` is your current username.

#### Configuring Docker
Further configuration can be added to the Docker setup, for example to start the Docker daemon on boot. Please refer to the general [Linux post-installation guide](https://docs.docker.com/engine/installation/linux/linux-postinstall) for more information. It also contains [troubleshooting information](https://docs.docker.com/engine/installation/linux/linux-postinstall/#use-a-different-storage-engine) in case you need it.

### Install Docker Compose
Docker Compose can be installed by following the [Install Docker Compose](https://docs.docker.com/compose/install/) guide on the Docker website. Please make sure to have Docker installed before installing this component.

In short, to install Docker Compose, first download the [latest release](https://github.com/docker/compose/releases/latest) from GitHub:

```sh
$ sudo curl -L https://github.com/docker/compose/releases/download/1.25.5/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
```

Then, apply the executable permissions to the downloaded binary:

```sh
$ sudo chmod +x /usr/local/bin/docker-compose
```

Test Docker compose by running the following command:

```sh
$ docker-compose --version
docker-compose version 1.25.5, build 8a1c60f6
```

The output should be similar as shown above.

## Install B2SHARE
Now the B2SHARE software package can be installed. It is located in the GitHub repository of EUDAT-B2SHARE and can be downloaded directly:

```sh
$ git clone https://github.com/EUDAT-B2SHARE/dockerize.git
```

<!--
Please make sure to add the specific release branch (e.g. `v2.0.1`) as an argument to the command, in order to not install the master branch which is used for development purposes.
-->

### Set environment variables
B2SHARE requires several environment variables that are used by the Docker containers to run. These need to be known before the containers are started.

##### Create a `setenv.sh` file
You can run add each variable using the `export` command individually, but it might be easier to create a file `setenv.sh` somewhere on your system or to add the environment variables directly to your `.bash_profile` file. It is advisable to enclose all values between single quotes to avoid problems in interpretation of these values.

For your convenience, a template `setenv.sh` file can be [downloaded](https://raw.githubusercontent.com/EUDAT-Training/B2SHARE-Training/master/deploy/setenv.sh) from this repository. Make sure to run the script as follows:

```sh
$ . ./setenv.sh
```

- Add the B2ACCESS OAuth client username and password:

```sh
export B2ACCESS_CONSUMER_KEY='username'
export B2ACCESS_SECRET_KEY='password'
```

- To encrypt user sessions a B2SHARE secret key must be set as an environment variable. It is recommended to use a randomly generated string for this purpose:

```sh
export B2SHARE_SECRET_KEY='some random key'
```

- Set the host domain for the JSON schemas callback, this should not include the protocol (e.g. `https://`):

```sh
export B2SHARE_JSONSCHEMAS_HOST='domain'
```

- Set up the PostgreSQL database database name and credentials. Note these are not the credentials you created for B2ACCESS access. You can fill in your own values here.

```sh
export B2SHARE_POSTGRESQL_DBNAME='dbname'
export B2SHARE_POSTGRESQL_PASSWORD='password'
export B2SHARE_POSTGRESQL_USER='user'
```

- Set a mount location for B2SHARE-related containers and data. This location does need to exist as it will be created by B2SHARE:

```sh
export B2SHARE_DATADIR='/home/ubuntu/b2share-data'
```

- Indicate whether the B2ACCESS production or development instance should be used. To use the development instance of B2ACCESS set this value to 1. For production installations, use the production instance of B2ACCESS and set this value to 0:

```sh
export USE_STAGING_B2ACCESS=1
```

- Make sure the database and indexes are properly initialized (value 1):

```sh
export INIT_DB_AND_INDEX=1
```

- If you want to load sample communities and records, set the following variable to 1:

```sh
export LOAD_DEMO_COMMUNITIES_AND_RECORDS=0
```

Please note that this will load several communities and records. If you need to have clean install, leave it to 0.

- Set the RabbitMQ user name and password. You can fill in your own values here.

```sh
export B2SHARE_RABBITMQ_USER='user'
export B2SHARE_RABBITMQ_PASS='pass'
```

##### Create a `.env` file
Another option is to create a `.env` file in the `dockerize` folder. Each variable can be added in a similar fashion, e.g.:

```
B2ACCESS_CONSUMER_KEY=username
```

**Note:** Make sure to remove all quotes and comments as these will be taken into the value for each variable as well.

A template `.env` file can be [downloaded](https://raw.githubusercontent.com/EUDAT-Training/B2SHARE-Training/master/deploy/.env) directly from this repository.

### The b2share.cfg file
Many settings are made directly in the Python `b2share.cfg` file, of which an example can be found [here](https://github.com/EUDAT-B2SHARE/v2-prod-instance/blob/master/b2share.cfg). Please refer to the [Services configuration](06_Services_configuration.md) guide to learn how this file can be used to configure your own B2SHARE instance.

## Building and running B2SHARE
Now that everything has been set up properly, the B2SHARE instance can be build:

```sh
$ sudo docker-compose build
```

Although there might be several reported problems, if the command is completed successfully, B2SHARE is ready to be launched.


### Running B2SHARE
To run B2SHARE and start the web service run the following command:

```sh
$ sudo docker-compose up -d
```

where the `-d` option indicates to start the containers in the background.

Now your own B2SHARE instance is available in your own domain! It might take a while before the service is fully running, so be patient and check back after a few minutes in your browser.

In the meantime you can see the actual output of all the container logs using the following command:

```sh
sudo docker-compose logs -f
```

where the `-f` option indicates to follow log output.

### Log into B2SHARE
To test the successful configuration of B2ACCESS within B2SHARE, try to log in with a user (not the OAuth client user). If there are no errors, your B2ACCESS configuration is correct.

## Troubleshooting
As with any installation of software or services, problems might arise. Refer to the [general troubleshooting](./B_Troubleshooting_and_known_issues.md) appendix to see if your problem can be solved.
