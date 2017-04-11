# B2SHARE REST API Python Training Module
<img align="right" src="../img/B2SHARE-logo.png" alt="B2SHARE logo" text="B2SHARE logo"> This training module provides training material and in-depth information in using the [EUDAT B2SHARE service](https://trng-b2share.eudat.eu) through application programming interfaces (APIs). It covers complete usage and implementation of the [B2SHARE REST API](https://b2share.eudat.eu/help/api) and provides step-by-step examples using Python. All functionality is also available in the web interface of B2SHARE, but the API allows integration of its functionality into your own workflows and applications.

All submodules have been set up to use the [B2SHARE training instance](https://trng-b2share.eudat.eu), which you can freely try and experiment with.

Please note that in order to use some functionality of the services you need to register your account and log in. Click [here](https://trng-b2share.eudat.eu/youraccount) to do so.

Although this module is complete, it is subject to change due to possible future alterations in the API specification. As soon as there are updates, this training module will be updated as well. In the meantime, you can check out the currently up-to-date [API implementation](https://b2share.eudat.eu/help/api) on the B2SHARE website.

### Prerequisites
This training modules assumes you have knowledge about data management basics such as depositing, metadata and persistent identifiers. In addition, all scripts are written in the [Python scripting](http://python.org) language. If you have no experience in programming or want to learn more about Python, it is highly recommended to follow [some](https://www.stavros.io/tutorials/python) [tutorials](http://pythonprogramminglanguage.com) or start [reading](https://en.wikibooks.org/wiki/Python_Programming) about it.

For trainees who do not have the possibility to install Python and the required Python packages, EUDAT provides pre-installed virtual machines in a training environment. To get access to this training environment, please use the [EUDAT contact pages](https://eudat.eu/support-request?service=DOCUMENTATION). Please provide some details on which community you are from and in which context you would like to follow the tutorial.

### Important remarks
The B2SHARE service makes a distinction between the two terms `record` and `draft record`. A record is published and therefore unchangeable and has persistent identifiers (PID) assigned to it, as well as checksums. A user can create a record by first creating a draft record, which is modifiable. Files and metadata can be placed into a draft record, but not into a published record.

In practice, a record is equivalent to a draft record when solely trying to read a record through the service API. Metadata of an existing published record can be updated by modifying the corresponding draft record and committing it as a new version of the original record.

### Submodules
Note: it it highly recommended to follow the guides in the given order. Later modules assume specific knowledge about Python and how to setup requests.

Submodule | Contents
------|-------------
[Introduction](00_Introduction.md) | General introduction to publishing data in B2SHARE
[Getting your API token](00_Getting_your_API_token.md) | Information on registration and creating your API tokens for usage with the Python scripts
[Retrieve record details](01_Retrieve_existing_record.md) | Learn how to get record information of specific existing records
[List existing records](02_List_existing_records.md) | Retrieve listings of records and paginate them
[Communities](03_Communities.md) | Community-specific functionality is explained
[Create new record](05_Create_new_record.md) | Learn how to create new records and add files and metadata
[Update record metadata](06_Update_record_metadata.md) | Learn how to update the metadata of existing records
[Special requests](08_Special_requests.md) | Various examples of special requests made using the API
[Example script](10_Example_script.md) | Example script with functions handling B2SHARE records
[Appendix A](A_Setup_and_install.md) | Setup and install guide for Python
[Appendix B](B_Request_and_Metadata_Reference_Guide.md) | Reference guide for API requests and record metadata

### Contact
If you encounter any problems or have any remarks, please contact EUDAT through the website [contact form](https://eudat.eu/contact) or [request support](https://eudat.eu/support-request?service=B2SHARE) directly.
