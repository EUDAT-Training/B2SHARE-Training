# Configuration
This module will take you through the configuration of your own B2SHARE instance.

The information on this page is based on the [B2SHARE installation guide](https://github.com/EUDAT-B2SHARE/b2share/blob/evolution/INSTALL.rst) provided by the developers. It covers:

- Configuring B2SHARE through the `b2share.cfg` file
- Additional configuration through the `config.py` file

## Configuring B2SHARE through the `b2share.cfg` file
Most of the configuration of B2SHARE is done in the `b2share.cfg` file. This file can be found in the `b2share` directory which is downloaded during the installation and deploy of the software package. See the relevant [installation documentation](04_Installation.md) for more information.

In this section all the services configuration options are omitted. They are described in the next module, [Services configuration](06_Services_configuration.md).

Each configuration is described by its keyword, e.g. `SUPPORT_EMAIL`. You have to locate the exact location in the configuration file. Any keywords that are not relevant for configuration are omitted as well.

### Basic configuration
Some options for emails, you can specify whether support emails are sent or that emails shouldn't be sent at all. For local instances a support email contact point needs to be set. When putting your B2SHARE instance into production, turn off mail send suppression.

```python
SUPPORT_EMAIL = None
MAIL_SUPPRESS_SEND = True
```

Specify where the logfiles are stored during migration:

```python
MIGRATION_LOGFILE = '/tmp/migration.log'
```

Specify the default timezone and language:

```python
BABEL_DEFAULT_LANGUAGE = 'en'
BABEL_DEFAULT_TIMEZONE = 'Europe/Zurich'
```

Configure the REST API endpoints for record manipulation:

```python
B2SHARE_RECORDS_REST_ENDPOINTS = dict(
    b2rec=dict(
        pid_type='b2rec',
        pid_minter='b2dep',
        pid_fetcher='b2rec',
        record_class='b2share.modules.records.api:B2ShareRecord',
        search_class=B2ShareRecordsSearch,
        record_serializers={
            'application/json': ('b2share.modules.records.serializers'
                                 ':json_v1_response'),
        },
        search_serializers={
            'application/json': ('b2share.modules.records.serializers'
                                 ':json_v1_search'),
        },
        links_factory_imp=('b2share.modules.records.links'
                           ':record_links_factory'),
        record_loaders={
            'application/json-patch+json': record_patch_input_loader,
            'application/json':
            lambda: request.get_json(),
        },
        default_media_type='application/json',
        list_route='/records/',
        item_route='/records/<pid(b2rec,record_class="b2share.modules.records.api:B2ShareRecord"):pid_value>',
        create_permission_factory_imp=CreateDepositPermission,
        read_permission_factory_imp=allow_all,
        update_permission_factory_imp=UpdateRecordPermission,
        delete_permission_factory_imp=DeleteRecordPermission,
    ),
)
```

Configure the REST API endpoints for deposits:

```python
DEPOSIT_PID = 'pid(b2dep,record_class="b2share.modules.deposit.api:Deposit")'
DEPOSIT_PID_MINTER='b2rec'
B2SHARE_DEPOSIT_REST_ENDPOINTS = dict(
    b2dep=dict(
        pid_type='b2dep',
        pid_minter='b2dep',
        pid_fetcher='b2dep',
        record_class='b2share.modules.deposit.api:Deposit',
        max_result_window=10000,
        default_media_type='application/json',
        record_serializers={
            'application/json': ('b2share.modules.deposit.serializers'
                                 ':json_v1_response'),
        },
        search_serializers={
            'application/json': (
                'b2share.modules.records.serializers:json_v1_search'),
        },
        links_factory_imp='b2share.modules.deposit.links:deposit_links_factory',
        record_loaders={
            'application/json-patch+json': deposit_patch_input_loader,
            'application/json':
            lambda: request.get_json(),
            # FIXME: create a loader so that only allowed fields can be set
            # lambda: request.get_json(),
            # 'b2share.modules.deposit.loaders:deposit_record_loader'
        },
        item_route='/records/<{0}:pid_value>/draft'.format(DEPOSIT_PID),
        create_permission_factory_imp=deny_all,
        read_permission_factory_imp=ReadDepositPermission,
        update_permission_factory_imp=UpdateDepositPermission,
        delete_permission_factory_imp=DeleteDepositPermission,
    ),
)
```

Define the indexer route to the right index and document type. The indexer can be found in `/b2share/modules/records/indexer.py`.

```python
INDEXER_RECORD_TO_INDEX='b2share.modules.records.indexer:record_to_index'
```

Set the permissions factory for records through the REST API. You can find all factories in the `/b2share/modules/records/permissions.py` file:

```python
#: Files REST permission factory
FILES_REST_PERMISSION_FACTORY = \
    'b2share.modules.files.permissions:files_permission_factory'
```

Set the sorting for the results when searching through the B2SHARE REST API. This will also affect the results shown in the search page.

```python
RECORDS_REST_DEFAULT_SORT = dict(
    records=dict(
        query='bestmatch',
        noquery='mostrecent',
    )
)
```

Define the available sort options shown in the search page of the web interface of B2SHARE:

```python
RECORDS_REST_SORT_OPTIONS = dict(
    records=dict(
        bestmatch=dict(
            fields=['-_score'],
            title='Best match',
            default_order='desc',
            order=1,
        ),
        mostrecent=dict(
            fields=['-_created'],
            title='Most recent',
            default_order='desc',
            order=2,
        ),
    ),
    deposits=dict(
        bestmatch=dict(
            fields=['-_score'],
            title='Best match',
            default_order='desc',
            order=1,
        ),
        mostrecent=dict(
            fields=['-_created'],
            title='Most recent',
            default_order='desc',
            order=2,
        ),
    )
)
```

Set the permissions factories for record manipulation through the REST API. You can find the factories in the `/b2share/modules/records/permissions.py` file:

```python
RECORDS_REST_DEFAULT_CREATE_PERMISSION_FACTORY = None
RECORDS_REST_DEFAULT_READ_PERMISSION_FACTORY = None
RECORDS_REST_DEFAULT_UPDATE_PERMISSION_FACTORY = None
RECORDS_REST_DEFAULT_DELETE_PERMISSION_FACTORY = \
    'b2share.modules.records.permissions:DeleteRecordPermission'
```

Set the permission factories for the accounts API. You can find the factories in the `/b2share/modules/users/permissions.py` file:

```python
ACCOUNTS_REST_ASSIGN_ROLE_PERMISSION_FACTORY = \
    'b2share.modules.users.permissions:RoleAssignPermission'
ACCOUNTS_REST_UNASSIGN_ROLE_PERMISSION_FACTORY = \
    'b2share.modules.users.permissions:RoleAssignPermission'
ACCOUNTS_REST_READ_ROLE_PERMISSION_FACTORY = authenticated_only
ACCOUNTS_REST_READ_ROLES_LIST_PERMISSION_FACTORY = authenticated_only

ACCOUNTS_REST_UPDATE_ROLE_PERMISSION_FACTORY = admin_only
ACCOUNTS_REST_DELETE_ROLE_PERMISSION_FACTORY = admin_only
ACCOUNTS_REST_CREATE_ROLE_PERMISSION_FACTORY = admin_only

# permission to list all the users having the specific role
ACCOUNTS_REST_READ_ROLE_USERS_LIST_PERMISSION_FACTORY = allow_all

# permission to list/search users
ACCOUNTS_REST_READ_USERS_LIST_PERMISSION_FACTORY = \
    'b2share.modules.users.permissions:AccountSearchPermission'

# permission to read user properties
ACCOUNTS_REST_READ_USER_PROPERTIES_PERMISSION_FACTORY = \
    'b2share.modules.users.permissions:AccountReadPermission'

# permission to update user properties
ACCOUNTS_REST_UPDATE_USER_PROPERTIES_PERMISSION_FACTORY = \
    'b2share.modules.users.permissions:AccountUpdatePermission'

# permission to list a user's roles
ACCOUNTS_REST_READ_USER_ROLES_LIST_PERMISSION_FACTORY = authenticated_only

ACCOUNTS_REST_ACCOUNT_LOADERS = dict(
    PATCH={
        'application/json': account_json_loader,
        'application/json-patch+json': account_json_patch_loader,
    }
)
```

Define the link to the Terms of Use of your B2SHARE instance. When set, this will be displayed in the UI in the footer:

```python
TERMS_OF_USE_LINK = 'http://hdl.handle.net/11304/e43b2e3f-83c5-4e3f-b8b7-18d38d37a6cd'
```

By default we suppose there is one proxy in front of B2SHARE. Configure it with the following keywords:

```python
WSGI_PROXIES = 1
PREFERRED_URL_SCHEME = 'http'
```

Define the maximum file size and record quota size:

```python
FILES_REST_DEFAULT_MAX_FILE_SIZE = 10 * 1024 * 1024 * 1024 # 10 GB per file
FILES_REST_DEFAULT_QUOTA_SIZE = 20 * 1024 * 1024 * 1024 # 20 GB per record
```

Set the site function to 'demo' or to 'production'. When 'demo' is set, this will be prominently shown on the front page and when using the REST API:

```python
SITE_FUNCTION = 'demo'
```

Use the `TRAINING_SITE_LINK` parameter to enable a message that will show up on the front page redirecting the testers to this link:

```python
TRAINING_SITE_LINK = ""
```

## Advanced configuration
The following configuration parameters are used to configure the security regarding the creation or manipulation of accounts:

```python
SECURITY_CONFIRMABLE=False
SECURITY_SEND_REGISTER_EMAIL=False
SECURITY_SEND_PASSWORD_CHANGE_EMAIL=False
SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL=False
```

## Additional configuration through the `config.py` file
This is similar to the section above. Will be expanded.

## Troubleshooting
As with any installation or configuration of software or services, problems might arise. Refer to the [general troubleshooting](./B_Troubleshooting_and_known_issues.md) appendix to see if your problem can be solved.
