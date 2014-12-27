Ticketus
--------

Ticketus is a simple, no-frills ticketing system for helpdesks. For more information, see [ticketus.org](http://ticketus.org/).

Requirements
============

* Python 3.3+
* PostgreSQL 9.3+
* WSGI server (e.g. gunicorn)
* Web server (e.g. nginx or Apache2)

Installation
============

1. Activate a virtualenv:

   ```
   $ virtualenv -p python3 ticketus
   $ cd ticketus && source bin/activate
   ```

2. Edit the configuration (copy `local_settings.py.example` to `local_settings.py` and edit).

3. Create and populate the database:

   ```
   $ createdb ticketus
   $ python manage.py migrate
   $ python manage.py collectstatic
   ```

4. Optionally import some data (see [import_scripts/README.md](https://github.com/sjkingo/ticketus/blob/master/import_scripts/README.md) for more information).

5. Point your WSGI server to `ticketus.wsgi.application`

