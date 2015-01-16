Ticketus
========

Ticketus is a simple, no-frills ticketing system for helpdesks. For more
information about its features and for a demo, see
[ticketus.org](http://ticketus.org/).

[![Latest Version](https://pypip.in/version/ticketus/badge.svg)](https://pypi.python.org/pypi/ticketus/)
[![Supported Python versions](https://pypip.in/py_versions/ticketus/badge.svg)](https://pypi.python.org/pypi/ticketus/)
[![Development Status](https://pypip.in/status/ticketus/badge.svg)](https://pypi.python.org/pypi/ticketus/)
[![License](https://pypip.in/license/ticketus/badge.svg)](https://pypi.python.org/pypi/ticketus/)

Requirements
------------

* Python 3.3+
* PostgreSQL 9.3+ and [psycopg2](http://initd.org/psycopg/)
* WSGI server (e.g. gunicorn)
* Web server (e.g. nginx or Apache2)

Installation
------------

1. Install your distro's packages for Python 3, virtualenv, and psycopg2. For 
   example, on Fedora:

   ```
   # yum install python3 python-virtualenv python3-psycopg2
   ```

2. Activate a virtualenv (ensure it uses Python 3 as 2.x is not supported):

   ```
   $ virtualenv -p python3 --system-site-packages ticketus
   $ cd ticketus && source bin/activate
   ```

3. Install the latest release from [PyPi](https://pypi.python.org/pypi/ticketus):

   ```
   $ pip install ticketus
   ```

4. Create a new Python package inside the virtualenv called `ticketus_settings` and copy the configuration to it:

   ```
   $ mkdir ticketus_settings
   $ touch ticketus_settings/__init__.py
   $ cp lib/python*/site-packages/ticketus/local_settings.py.example ticketus_settings/local_settings.py
   ```

5. Edit the settings and specify at least the database and `BASE_DIR` (which should be set to the full path to the virtualenv).

6. Create and populate the database:

   ```
   $ createdb ticketus
   $ PYTHONPATH=. ticketus-admin init
   ```

   Note when running `ticketus-admin`, you must set `PYTHONPATH` to the parent directory of where `ticketus_settings` is located.

7. Optionally import some data (see [import_scripts/README.md](https://github.com/sjkingo/ticketus/blob/master/import_scripts/README.md) for more information).

8. Point your WSGI server to `ticketus.wsgi`, e.g.:

   ```
   $ pip install gunicorn
   $ gunicorn ticketus.wsgi
   ```

9. You must point your web server to serve files from `static`, as gunicorn will not.

10. If you just wish to bring up the development server quickly for testing, run:

   ```
   $ PYTHONPATH=. ticketus-admin runserver
   ```

LDAP authentication
-------------------

LDAP authentication is available by using the `django_auth_ldap3` library. Follow the 
[installation instructions](https://github.com/sjkingo/django_auth_ldap3) to set up.

Email gateway
-------------

Ticketus provides an email gateway for retrieving emails and importing them as
tickets and comments. Currently there exists a backend for IMAP4 and it can be
run as a cronjob.
