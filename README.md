Ticketus
========

Ticketus is a simple, no-frills ticketing system for helpdesks. For more information, see [ticketus.org](http://ticketus.org/).

The latest "stable" release is `0.5-beta`.

[![Build Status](https://travis-ci.org/sjkingo/ticketus.svg)](https://travis-ci.org/sjkingo/ticketus) [![Requirements Status](https://requires.io/github/sjkingo/ticketus/requirements.svg?branch=master)](https://requires.io/github/sjkingo/ticketus/requirements/?branch=master)

Requirements
------------

* Python 3.3+
* PostgreSQL 9.3+
* WSGI server (e.g. gunicorn)
* Web server (e.g. nginx or Apache2)

Installation
------------

1. Activate a virtualenv:

   ```
   $ virtualenv -p python3 ticketus
   $ cd ticketus && source bin/activate
   ```

2. Install the system requirements inside the virtualenv:

   ```
   $ pip install -r requirements.txt
   ```

3. Edit the configuration (copy `local_settings.py.example` to `local_settings.py` and edit).

4. Create and populate the database:

   ```
   $ createdb ticketus
   $ python manage.py migrate
   $ python manage.py collectstatic
   ```

5. Optionally import some data (see [import_scripts/README.md](https://github.com/sjkingo/ticketus/blob/master/import_scripts/README.md) for more information).

6. Point your WSGI server to `ticketus.wsgi.application`

