# User management
This guide will dive into the management of users in B2SHARE.

Topics covered:
- User management principles
- B2ACCESS user registration
- Setting user roles

### Registering a new user for B2SHARE
Once you've successfully set up B2ACCESS, you can continue with the registration of a administrative user that will be able to configure B2ACCESS.

For testing purposes, a different user can be registered which can be used to log in to your own B2SHARE instance and upload new records. Again go to the [B2ACCESS acceptance instance](https://unity.eudat-aai.fz-juelich.de:8443/home/home) and click on 'Register a new account'. Now select 'EUDAT staff' and fill out the form.

Alternatively, you can use your social ID or institutional credentials by selecting the corresponding authentication option when logging in to B2SHARE.

## Setting user roles
A registered user can have specific roles in B2SHARE that allows it to e.g. create new records, administer community information and reviewing records.

### Set the super administrator
The superadministrator right allows a particular user to run any B2SHARE operation. Please be careful in assigning it.

Please note: all role operations identify the user based on the email address. The user must therefore have logged in into B2SHARE instance at least once in order to be known by the system.

#### Add super administration rights
The super administration privileges are set using the b2share tool using the `access` command:

```sh
$ b2share access allow -e <email_address> superuser-access
```

where the argument `email_address` is the email address of the user you want to give administrator privileges to. The command will not give any response even if it successfully added the rights. To see the actual

### List current user rights
You can list whether a user has super administrator rights by the following command:

```sh
$ b2share access show -e <email_address>
user:<email_address>:superuser-access::allow
```

If there is no listing, it means that no user has super administration rights.

### Remove super administration rights
If you want to revoke the super administration rights of a specific user, the following command with similar arguments does exactly that:

```sh
$ b2share access remove -e <email_address> superuser-access
```

where `email_address` is the email address of the user.
