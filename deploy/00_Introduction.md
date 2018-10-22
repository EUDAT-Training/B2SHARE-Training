# Introduction
Before B2SHARE is actually installed and deployed, it is important to learn how B2SHARE is structured.

### B2SHARE container services
B2SHARE connects to several internal services in order to run properly:
- redis
- elasticsearch
- a database engine (postgresql or mysql)
- rabbitmq

To simplify the creation of this required execution environment, the Docker containers are used using the Docker application engine.

The default Docker configuration for B2SHARE will try to mount a folder from the host machine your B2SHARE instance is running on. This folder is used to store all the data uploaded into B2SHARE and is therefore very important.

### B2SHARE connected services
Although B2SHARE is a stand-alone service, it is dependent on several other services in order to function properly:
- For user management, administration and authentication, EUDAT's [B2ACCESS service](https://b2access.eudat.eu) is used
- For minting, administration and resolving of EPIC persistent identifiers or handles, EUDAT's [B2HANDLE service](https://www.eudat.eu/services/userdoc/b2handle) is used
- EUDAT's [B2DROP](https://b2drop.eudat.eu) can be integrated to directly publish files from this service into B2SHARE
- Alternative identifiers are minted and resolved using the [Digital Object Identifier](http://doi.org) (DOI) service
- Semantic annotation for files published in B2SHARE records is possible using EUDAT's [B2NOTE service](https://eudat.eu/news/annotate-your-research-data-with-b2note)

Refer to the dedicated [Services configuration](06_Services_configuration.md) guide on how to configure each of these services.