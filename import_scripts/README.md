import_scripts
==============

This directory contains scripts for importing tickets and comments from
external ticketing systems into Ticketus. They depend on a working and 
configured application (so please perform the initial migration as per
installation docs before using these scripts).

Each script has a docstring at the top explaining how it works and how to
use it. Additionally, you may execute the script with `-h` argument to view
syntax and argument help.

Some general considerations to note that apply to all import scripts:

* They are non-destructive. This means they will not alter any existing data
  in the database, nor will they conflict with any existing tickets or comments.

* If you do wish to start with a "clean slate" - run the following command:
   
  `$ python manage.py sqlflush | psql DB_NAME`

  Please note this will **DESTROY** the database and all tickets, comments, tags
  and users (including superusers!). Use at your own risk.
  
* Typically, the scripts can be run multiple times without duplicates being created.
  You can safely run them over and over to "sync" up the local tickets, as most scripts
  will update any existing data they import if it already exists.

* Each script uses its own way of determining if a ticket in the external system
  exists in the local database. See the script's documentation for more information.

List of scripts
===============

* [github.py](https://github.com/sjkingo/ticketus/blob/master/import_scripts/github.py) - import from a GitHub repo's issues
* [dogfood_generator.sh](https://github.com/sjkingo/ticketus/blob/master/import_scripts/dogfood_generator.sh) - syncs GitHub issues for Ticketus to the local database
* [freshdesk.py](https://github.com/sjkingo/ticketus/blob/master/import_scripts/freshdesk.py) - import from a Freshdesk helpdesk
