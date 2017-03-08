# Introduction
Before B2SHARE is actually installed and deployed

## B2SHARE container services
B2SHARE connects to several external services in order to run properly:
- redis
- elasticsearch
- a database engine (postgresql or mysql)
- rabbitmq

To simplify the creation of this required execution environment, the Docker containers are used using the Docker application engine.

The default Docker configuration for B2SHARE will try to mount a folder from the host machine your B2SHARE instance is running on. This folder is used to store all the data uploaded into B2SHARE and is therefore very important.

