# Themeing
B2SHARE has a default look that is tailored towards EUDAT. If you are running your own instance you can change the look to your institute's or own liking by simply altering the files that define the theme of B2SHARE.

This guide covers:
- Structure of theme and pages
- Location of thematic files
- What to change where
- Testing your changes

### Prerequisites
Please make sure that you have following all previous submodules as far as necessary and that your B2SHARE instance is correctly running.

## Structure of B2SHARE theme
B2SHARE provides a separate layer in the codebase that defines and render the layout.

The web interface of B2SHARE is built as a single page application that renders all content based on the requested information by the user. All interaction is programmed in [ReactJS](https://reactjs.org) which is converted to JavaScript upon running your instance.

### Page updates
Many of the interaction with the server and other services is programmed directly in the Javascript. When a page is called the follow procedure is followed:
1. A user event or page load event trigger an AJAX query from the server
    - All server events are handled in `src/data/server.js`
2. The callback of the AJAX call places the data returned from the server in an immutable data store
3. Each update of an object changing values in the data store automatically triggers a new repaint of the application
    - See `src/main.jsx`, `updateStateOnTick` in `AppFrame`
4. The application repaint procedure uses the data from the store as parameters for the react components

## Folder structure
All thematic files are located (in subfolders) of the folder `webui`. This is at the same time the root path of the public path of the webserver.

The deployment of the theme is defined in the file `package.json`. This can be left untouched unless you need new packages for additional functionality in your theme. If you fire up the Docker containers of B2SHARE, this file will be processed using the `composer` tool. It includes the copying of some files located in the `node_modules` folder that is created when downloading all packages.

There are two configuration files provided: `webpack.config.devel.js` and `webpack.config.js` of which the latter is used during production. This first file can be used during development when firing up a webpack server process. See the section [Testing your changes](#testing-your-changes) below.

## Testing your changes
When running your instances all thematic files are packed into a single where possible by the package `webpack`.

If you don't want to run the full instance but just want to test your changes to static parts of the theme, you can also run a separate server process for showing the interface.