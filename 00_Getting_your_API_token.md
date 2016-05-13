# Getting you API token
This guide will make sure you have an API token which is required to access the B2SHARE service programmatically. Every time you access the service using a script or application, you need to identify yourself using a generated personal access token. This token can be retrieved using the B2SHARE service website.

## Setup your machine and connection
Please make sure your machine has been properly setup to use Python and required packages. Follow [this](A_Setup_and_install.md) guide in order to do so.

## Account registration
This guide assumes you have successfully registered your account on B2SHARE using your institutional credentials through B2ACCESS.

## The account page
Go to the [B2SHARE website](https://b2share.eudat.eu). After logging in, navigate to your [account page](https://b2share.eudat.eu/youraccount/display) by clicking on your name on the home page of B2SHARE.

Click on the wrench next to 'Account' to go to your [profile settings page](https://b2share.eudat.eu/account/settings/profile). Select the bottom option in the left menu to go to the application and token [settings page](https://b2share.eudat.eu/account/settings/applications). Here you can register new application and tokens to use within your own applications and scripts.

<img src="img/B2SHARE-applications.png" alt="B2SHARE account applications and tokens" text="B2SHARE account applications and tokens" style="width: 80%">

## API token generation
Click on the 'New token' button to generate a new personal access token. Enter a name which easily identifies the purpose for this key. By clicking 'Create' a new token is generated which is only shown at this time. Store it somewhere in order to use later, like in a file. In this training material it is assumed that the generated token is stored in a file called `token`.

<img src="img/B2SHARE-generate-token.png" alt="B2SHARE generate token" text="B2SHARE generate token">

Click 'Save' to store the token on the server as well in order to make it usable in your applications.
