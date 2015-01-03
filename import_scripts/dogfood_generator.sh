#!/bin/bash

# Wipes out the local database and populates it with the GitHub issues
# for the Ticketus project. 'Eat Your Own Dog Food' and all that.
# You will probably want to create a new superuser after this runs.

../manage.py sqlflush | psql ticketus
./import_github.py sjkingo ticketus
