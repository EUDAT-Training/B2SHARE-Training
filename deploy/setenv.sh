#!/bin/bash

export B2ACCESS_CONSUMER_KEY='username'             # B2ACCESS user name
export B2ACCESS_SECRET_KEY='password'               # B2ACCESS password
export B2SHARE_SECRET_KEY='some random key'         # B2SHARE secret key

export B2SHARE_JSONSCHEMAS_HOST='domain'            # schemas host domain

export B2SHARE_POSTGRESQL_DBNAME='dbname'           # postgres database name
export B2SHARE_POSTGRESQL_USER='user'               # postgres database user name
export B2SHARE_POSTGRESQL_PASSWORD='password'       # postgres database password

export B2SHARE_DATADIR='/home/ubuntu/b2share-data'  # the local shared data folder in which all data is stored

export USE_STAGING_B2ACCESS=1                       # to run with staging (testing) B2ACCESS (unity install)

export INIT_DB_AND_INDEX=1                          # when run the first time, initialize the database and indices
export LOAD_DEMO_COMMUNITIES_AND_RECORDS=0          # set to 1 to load demo object upon deploy

export B2SHARE_RABBITMQ_USER='user'                 # RabbitMQ user name
export B2SHARE_RABBITMQ_PASS='pass'                 # RabbitMQ password
