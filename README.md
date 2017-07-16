# How to install and run the FROG4 Migration Orchestrator

This document presents how to install and run the FROG4 Migration Orchestrator.

## Install dependencies

```sh
        $ sudo apt-get install python3-setuptools python3-dev python3-pip git
        $ sudo pip3 install gunicorn flask flask-restplus
```

## Clone the code

```sh
        $ git clone https://github.com/netgroup-polito/frog4-migration-orch
        $ cd frog4-migration-orch
```

## Configuration file

In order to properly configure the migration orchestrator, you should edit the follwoing files:
- [configuration file](https://github.com/netgroup-polito/frog4-migration-orch/blob/master/config/default-config.ini): includes the general settings of the module.
- [app-config](https://github.com/netgroup-polito/frog4-migration-orch/blob/master/web_gui/static/appConfig.js): contains the parameters that are required only if you need to use the web-gui to show the migration process. If you want to use the migration orchestrator without the gui you don't need to edit this file.

## Start

```sh
        $ ./start.sh
```

When the component is started, you can use it through the GUI at url: http://address:port/gui, or directly through the REST API. 
In addition, the swagger-generated documentation of the API is available at http://address:port/api_docs.
