# Troubleshooting and Known Issues
This page serves as a overview of all the known issues that might arise while using your own instance of B2SHARE.

The following issues are described:
- [The postgres Docker container is not able to create the database files](#the-postgres-docker-container-is-not-able-to-create-the-database-files)
- [B2ACCESS connection problems upon login](#b2access-connection-problems-upon-login)

## Troubleshooting
In this section any issues that can be solved are described.

### The postgres Docker container is not able to create the database files

#### Problem
Upon install, the Docker container which contains the postgres database software, complains about missing file/directory access permissions.

#### Possible cause
Access to the `B2SHARE_DATADIR` mount location is blocked by [SELinux](https://wiki.centos.org/HowTos/SELinux) if this Linux module is enabled in for example CentOS.

#### Solution
Modify the volume definitions in the `docker-compose.yml` file in the `dockerize` folder by appending the `:Z` option to it, e.g.:

```
$(B2SHARE_DATADIR)/postgres-data:/var/lib/postgresql/data`
```

becomes

```
$(B2SHARE_DATADIR)/postgres-data:/var/lib/postgresql/data:Z
```

This postfix makes sure only the 

### B2ACCESS connection problems upon login

#### Problem
If you experience any problems during logging in into your B2SHARE instance, there might be problem with the B2ACCESS configuration. A common error might be displayed while access B2SHARE:

```
 ERROR

OAuth Authorization Server got an invalid request.

If you are a user then you can be sure that the web application you was using previously is either misconfigured or buggy.

If you are an administrator or developer the details of the error follows:

The '<username>' requested to use a not registered response redirection URI: <OAuth URL>
```

#### Probable cause
This means that your B2ACCESS OAuth URL is not properly configured, probably due to an erroneous domain name or incorrect endpoint. 

#### Solution
Please visit the corresponding B2ACCESS instance (see [above](#different-b2access-instances), log in with your OAuth Client user and enter the correct URL in the `OAuth client return URL` field.

## Known Issues
In this section any issues that are known but currently cannot be solved are listed.

There are currently no known issues.