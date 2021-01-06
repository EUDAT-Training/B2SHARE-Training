# Maintenance
It is very important to keep your instance in a good shape. Many aspects need to be taken in consideration during the running of your instance.

This guide covers:
- Cleaning up stored files of removed records

### Prerequisites
Please make sure that you have following all previous submodules and that your B2SHARE instance is correctly running.

All commands below are using the [b2share tool](A_b2share_Tool_Reference.md#general-syntax) after successfully [entering](08_Configuration.md#entering-the-docker-container-environment) the B2SHARE Docker container.

## Cleaning up stored files of removed records
If a (draft) record is removed, the record information in the database will be marked as 'deleted'. It will _not_ remove the files associated with the record for safety reasons and to be able to restore a removed record. There is currently no command to get these files removed, but if you really want to do this, you can follow these steps.

**TAKE THESE STEPS AT YOUR OWN RISK! POTENTIALLY, DELETED FILES CAN NO LONGER BE RESTORED**

### Locating the file storage location
It will be necessary to enter your database environment and to determine where the file storage location is. If you are running your instance using a Docker container environment, the storage location os configured in the environment (`.env`) and composition (`docker-compose.yml`) files.

Files are stored in the `/usr/var/b2share-instance/files` folder, unless this has been changed to a different location.

There is possibly a line similar to this that maps the files location in the `b2share` container to a file location on your physical node:

```yaml
      - "${B2SHARE_DATADIR}/b2share:/usr/var/b2share-instance"
```

This way the files can be managed on the physical system as well.

### Understanding the file path structure
For every file uploaded to B2SHARE into a given (draft) record, a new folder will be created in the files storage location folder. Every file internally has an identifier known as the file ID. This identifier is reflected in the storage path of a given file, e.g. when a file has identifier `aa490190-6b60-4957-897b-9f0720c02612` it will be stored as `aa/49/0190-6b60-4957-897b-9f0720c02612/data` in the files storage location. The exact path structure depends on the configuration set in the Invenio settings, but the default settings will be assumed.

It is therefore possible that multiple files belonging to different records are stored in the same first part of some path based on the identifier of these files.

### Finding orphaned files
Once a (draft) record is deleted, the files belonging to the corresponding file bucket and record version are no longer linked to the record itself. To find any orphaned files - belonging to removed records -, the following query can be executed in your database environment (potentially a separate container in your setup):

```sql
select id, uri, size, checksum from files_files where id not in (select file_id from files_object);
```

This will for example show the following result (in PostgreSQL):

```sh
                  id                  |                                        uri                                         |  size   |               checksum
--------------------------------------+------------------------------------------------------------------------------------+---------+--------------------------------------
 68de5603-a5ab-40b7-a9e0-15a7689f5cd6 | file:///usr/var/b2share-instance/files/68/de/5603-a5ab-40b7-a9e0-15a7689f5cd6/data |     692 | md5:830742d6224740b2cfee1449e0706e97
 ed97ef41-1c16-4e70-aa67-ef23a59e8847 | file:///usr/var/b2share-instance/files/ed/97/ef41-1c16-4e70-aa67-ef23a59e8847/data | 8606595 | md5:29f79ac7851f8b9fa34e0e6419533a8b
 645318c8-4f77-4575-a536-69d9b26df95a | file:///usr/var/b2share-instance/files/64/53/18c8-4f77-4575-a536-69d9b26df95a/data |     692 | md5:830742d6224740b2cfee1449e0706e97
 b3b9c4b9-ef07-44dd-a31e-22d216e5ffcc | file:///usr/var/b2share-instance/files/b3/b9/c4b9-ef07-44dd-a31e-22d216e5ffcc/data |     692 | md5:830742d6224740b2cfee1449e0706e97
 b2051470-ca12-48d1-af1f-4b54eeb8a8fc | file:///usr/var/b2share-instance/files/b2/05/1470-ca12-48d1-af1f-4b54eeb8a8fc/data |     692 | md5:830742d6224740b2cfee1449e0706e97
 2837a920-86da-446e-931b-f010f0c15a9b | file:///usr/var/b2share-instance/files/28/37/a920-86da-446e-931b-f010f0c15a9b/data |     692 | md5:830742d6224740b2cfee1449e0706e97
 aa490190-6b60-4957-897b-9f0720c02612 | file:///usr/var/b2share-instance/files/aa/49/0190-6b60-4957-897b-9f0720c02612/data |     692 | md5:830742d6224740b2cfee1449e0706e97
 eaa870d9-af5b-44f8-ae9e-cc622b3499e2 | file:///usr/var/b2share-instance/files/ea/a8/70d9-af5b-44f8-ae9e-cc622b3499e2/data |     692 | md5:830742d6224740b2cfee1449e0706e97
 3645e41b-fe26-40ac-8096-d64ea5062e63 | file:///usr/var/b2share-instance/files/36/45/e41b-fe26-40ac-8096-d64ea5062e63/data |     692 | md5:830742d6224740b2cfee1449e0706e97
 cda21eec-7101-47f6-b2b3-717274cecd09 | file:///usr/var/b2share-instance/files/cd/a2/1eec-7101-47f6-b2b3-717274cecd09/data |     692 | md5:830742d6224740b2cfee1449e0706e97
 693b19da-9b4e-47dd-996e-84716e5c0496 | file:///usr/var/b2share-instance/files/69/3b/19da-9b4e-47dd-996e-84716e5c0496/data |     692 | md5:830742d6224740b2cfee1449e0706e97
 07139600-cd34-40d6-b835-1b7c4b9784f7 | file:///usr/var/b2share-instance/files/07/13/9600-cd34-40d6-b835-1b7c4b9784f7/data |     692 | md5:830742d6224740b2cfee1449e0706e97
 a649e9df-912e-47fa-a3c2-3a42f5f15873 | file:///usr/var/b2share-instance/files/a6/49/e9df-912e-47fa-a3c2-3a42f5f15873/data |     692 | md5:830742d6224740b2cfee1449e0706e97
 c4cfea04-b458-4723-a42c-de54e92b0c20 | file:///usr/var/b2share-instance/files/c4/cf/ea04-b458-4723-a42c-de54e92b0c20/data |     692 | md5:830742d6224740b2cfee1449e0706e97
 293aea90-2a58-4e9c-a80c-0b6ce6bfafd0 | file:///usr/var/b2share-instance/files/29/3a/ea90-2a58-4e9c-a80c-0b6ce6bfafd0/data |     692 | md5:830742d6224740b2cfee1449e0706e97
 a26f1cb4-c34c-4c17-8d7e-3c9c98d361ad | file:///usr/var/b2share-instance/files/a2/6f/1cb4-c34c-4c17-8d7e-3c9c98d361ad/data |     692 | md5:830742d6224740b2cfee1449e0706e97
 7ddaf78a-2d5f-4ce9-9079-921e7f81eb3c | file:///usr/var/b2share-instance/files/7d/da/f78a-2d5f-4ce9-9079-921e7f81eb3c/data |     692 | md5:830742d6224740b2cfee1449e0706e97
 82ed8122-939c-4c9f-8600-b20dadacef94 | file:///usr/var/b2share-instance/files/82/ed/8122-939c-4c9f-8600-b20dadacef94/data |     692 | md5:830742d6224740b2cfee1449e0706e97
 ```

 The files shown are no longer tied to any record and therefore can be deleted. The values in the `uri` column show the actual storage location of the file. Use the values in the `size` and `checksum` column to make sure you are handling the right files on your storage system.

 Be aware that multiple files can reside in the same folders to some extent in the path structure. So be sure to only remove the file named `data` in a given folder, and not to remove the complete path.