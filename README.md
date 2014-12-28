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

1. Install your distro's packages for Python 3, virtualenv, and psycopg2. For 
   example, on Fedora:

   ```
   yum install python3 python-virtualenv python3-psycopg2
   ```

1. Activate a virtualenv (ensure it uses Python 3 as 2.x is not supported):

   ```
   $ virtualenv -p python3 --system-site-packages ticketus
   $ cd ticketus && source bin/activate
   ```

2. Install the latest "stable" release of ticketus from GitHub:

   ```
   $ git clone http://github.com/sjkingo/ticketus.git
   $ cd ticketus
   $ git checkout v0.5-beta
   ```

   (if you wish to use the latest bleeding-edge version, you may leave out the last line and instead use `master`.)

3. Install the dependencies:

   ```
   $ pip install -r requirements.txt
   ```

4. Edit the configuration (copy `ticketus/local_settings.py.example` to `ticketus/local_settings.py` and edit).

5. Create and populate the database:

   ```
   $ createdb ticketus
   $ python manage.py migrate
   $ python manage.py collectstatic
   $ python manage.py createsuperuser
   ```

6. Optionally import some data (see [import_scripts/README.md](https://github.com/sjkingo/ticketus/blob/master/import_scripts/README.md) for more information).

7. Point your WSGI server to `ticketus.wsgi`, e.g.:

   ```
   $ pip install gunicorn
   $ gunicorn ticketus.wsgi
   ```

8. You must point your web server to serve files from `ticketus/static`, as gunicorn will not.

9. If you just wish to bring up the development server quickly for testing, run:

   ```
   $ python manage.py runserver
   ```

