# Services configuration
Several services are connected to B2SHARE in order to make it function smoothly. In this guide the configuration of each of these services is described.

In this guide the following services are discussed:
- [B2ACCESS](#Configuring+B2ACCESS): use institional or social credentials for access using EUDAT's [federated authentication and authorisation service](https://b2access.eudat.eu)
- [B2HANDLE](#Configuring+B2ACCESS): registration and resolving of EPIC handles using EUDAT's [persistent identifier service](https://www.eudat.eu/services/userdoc/b2handle)
- [B2DROP](#Configuring+B2DROP): direct publication from EUDAT's [data sharing and exchange service](https://b2drop.eudat.eu)
- [DOI](#Configuring+Digital+Object+Identifier+DOI+service): registration and resolving of [DOI persistent identifiers](http://www.doi.org)
- [B2NOTE](#Configuring+B2NOTE): adding metadata to files using EUDAT's [semantic annotation service](https://b2note.bsc.es) (in pilot phase)

## Configuring B2ACCESS
In this section the configuration of B2ACCESS is described.

### Different B2ACCESS instances
Currently there are two instances of B2ACCESS running:

- An [acceptance (testing) instance](https://unity.eudat-aai.fz-juelich.de:8443/home/home) run by [Jülich Forschungszentrum](http://www.fz-juelich.de)

This instance can be used to test your instance. Any user registration request will be automatically granted and therefore can be immediately used.

- The [production instance](https://b2access.eudat.eu/home/home) run by EUDAT

The production instance of B2ACCESS can only be used for production instance of B2SHARE. You registration requests will only be granted if sufficient information is provided that you need an actual production registration.

For the remaining part of this guides and all other guides, it is assumed that the B2ACCESS acceptance instance is used. For more information on B2ACCESS and its configuration, please refer to the EUDAT user documentation on [B2ACCESS service integration](https://eudat.eu/services/userdoc/b2access-service-integration).

### Registering your B2ACCESS OAuth 2.0 client
To let B2SHARE automatically communicate with B2ACCESS a OAuth 2.0 Client registration is required.

- Go to the [B2ACCESS acceptance instance](https://unity.eudat-aai.fz-juelich.de:8443/home/home) and click on 'Register a new account' (top-right):

<img width="100%" src="img/B2ACCESS-client-registration.png" alt="B2ACCESS OAuth 2.0 client registration" text="B2ACCESS OAuth 2.0 client registration">

- Click 'OAuth 2.0 Client Registration Form' and fill in a user name, passwords, security question answers and your email address:
 - Carefully remember your username and password, as this will be needed later on (see [below](#set-environment-variables))

<img width="100%" src="img/B2ACCESS-oauth-form.png" alt="B2ACCESS OAuth 2.0 registration form" text="B2ACCESS OAuth 2.0 registration form">

- Take special care for the OAuth client return URL. This needs to be your fully qualified domain name (FQDN) plus the API endpoint for B2ACCESS in the B2SHARE service, e.g.:

```
https://my-domain.com/api/oauth/authorized/b2access/
```

This value can always be changed later by logging in to B2ACCESS again with the newly created credentials.

- Upon successfull registration, you will see the following overview:

<img width="100%" src="img/B2ACCESS-oauth-overview.png" alt="B2ACCESS OAuth 2.0 registration overview" text="B2ACCESS OAuth 2.0 registration overview">

### Registering a new user for B2SHARE
Once you've successfully set up B2ACCESS, you can continue with the registration of a administrative user that will be able to configure B2ACCESS.

For testing purposes, a different user can be registered which can be used to log in to your own B2SHARE instance and upload new records. Again go to the [B2ACCESS acceptance instance](https://unity.eudat-aai.fz-juelich.de:8443/home/home) and click on 'Register a new account'. Now select 'EUDAT staff' and fill out the form.

Alternatively, you can use your social ID or institutional credentials by selecting the corresponding authentication option when logging in to B2SHARE.

## Configuring B2HANDLE
In this section the configuration of B2HANDLE is described.

## Configuring B2DROP
In this section the configuration of B2DROP is described.

## Configuring Digital Object Identifier (DOI) service
In this section the configuration of the Digital Object Identifier (DOI) service is described. With this service new DOIs can be minted, administered and resolved.

## Configuring B2NOTE
In this section the configuration of B2NOTE is described.
