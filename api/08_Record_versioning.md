# Record versioning
In most cases it is not necessary to change, remove or add new files to a record. In fact, this is not possible without creating a new version of that record. In this guide, the files of an existing record are updated, thereby creating a new draft record. A JSON patch is prepared that will publish this new draft record. The published record will have different EPIC PIDs and DOIs than the original record. In the metadata there will be a reference to the old version.

As updates to metadata are exactly the same as for record or draft records, this is not discussed in this submodule. Please refer to the [Update record metadata](06_Update_record_metadata.md) and [Update all community metadata](07_Update_all_community_metadata.md) guides for information on how to do this.

This guide covers:
- Creating a new draft record from an existing published record
- Altering the files attached to the record
- Submitting a JSON patch to publish the new version
- Investigating the links to

