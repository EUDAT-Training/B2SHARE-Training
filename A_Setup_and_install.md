# Install and setup the required software your machine
This document describes the necessary steps to make your machine ready for using Python and connecting to the B2SHARE service.

## Prerequisites
You need a machine equipped with an internet connection and a recent version of the Python software package (version >= 2.7) and the Package Installer for Python (pip) which is installed with the newest versions of Python.

You can check whether you have Python installed by entering the following command:
```sh
python --version
```

Please make sure your system is up-to-date and has installed the latest security updates.

### Software
Depending on the operating system you are using, Python can be installed by either downloading it from the official [Python website](http://python.org), or using a package manager (non-Windows only). For Linux-typed systems, a package manager comes pre-installed, for OS X, it needs to be downloaded.

#### Linux
For example, to install Python on Ubuntu, do the following:
```sh
apt-get install python
```

#### OS X
For OS X, use the package manager [Brew](http://brew.sh). It can be downloaded through the website or directly by
```sh
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Then install Python using this package manager:
```sh
brew install python
```

#### Windows
For Windows-enabled machines, go to the Python [download page](https://www.python.org/downloads/). Download either the 2.7 or 3.x version and install it.

### Package Installer for Pyton (pip)
Python comes with a great bundle of functionality and can be extended by Python packages. You can install Python packages by using the Package Installer for Python (pip). You can check whether pip is installed on your system by issuing the following command:
```sh
pip --version
```

If you don't get a proper response with a version number, pip is not installed and you need to install it by following this [guide](https://pip.pypa.io/en/latest/installing). The quick route is to get the install script directory and execute it using Python:
```sh
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
```

## Packages
Once Python is installed on your machine, a package need to be installed additionally in order to get access to the B2SHARE service.

The following packages are required:
```sh
requests
```

## Machine setup
No additional setup is required in order to run Python or the provided script snippets.
