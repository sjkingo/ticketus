#!/usr/bin/env python

"""Import script for GitHub Issues to Ticketus.

This script requires some added libraries. If they are not installed you will
need to install them first using pip:

 * -e git+https://github.com/sigmavirus24/github3.py.git#egg=github3.py
 * html2text
 * pytz

This is *not* a destructive operation. This script will not delete any existing
issues; instead each ticket will be created with the `imported_key` field set
to the unique URI given by GitHub for each issue.. This means you do not need
to ensure uniqueness with any existing tickets. Each time the script is run,
new tickets will be added and no duplicates will be created.

You must specify a repository owner and repository name as arguments, and
optionally a username and password if the repository is private. If 2FA is
enabled on your account, you must specify --2fa and you will be prompted for
your authentication code. NOTE that this is interactive!!!

Please note annonymous access (no username and password) is rate-limited heavily
by GitHub. It is recommended you authenticate to get around this.

Please see https://developer.github.com/v3/#rate-limiting for more information.
"""

# Check that the github3.py library is installed.
_gh3_install_cmd = 'pip install -e git+https://github.com/sigmavirus24/github3.py.git#egg=github3.py'
try:
    from github3 import GitHub, login, __version__ as __gh_version__
except ImportError:
    print('ERROR: github3.py is not installed. Please run (inside a virtualenv):')
    print('  ' + _gh3install_cmd)
    exit(1)
if not __gh_version__.startswith('1.'):
    print('ERROR: github3.py version 1.0 or higher is not installed. Instead version {} is installed.'.format(github3.__version__))
    print('Please remove it and run (inside a virtualenv):')
    print('  ' + _gh3_install_cmd)
    exit(1)

# Import django
import os.path, sys
sys.path.append(os.path.realpath('..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticketus.settings')
import django
django.setup()

import datetime
from html2text import html2text
import pytz

from django.contrib.auth.models import User
from ticketus.core.models import *

def labels_list(issue):
    """Returns a list of labels (tag names) in the given issue."""
    return [x['name'] for x in issue['labels']]

def get_user(username):
    """Given a username, gets or creates it in the local database and returns
    the User instance."""
    user, created = User.objects.get_or_create(username=username)
    return user

_tz = pytz.timezone('Australia/Brisbane')
def timestamp_to_local(timestamp):
    """Given a str timestamp, convert it to a datetime object with correct
    timezone information (as GitHub uses UTC)."""
    naive = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
    return naive.astimezone(_tz)

def authenticate_with_github(username=None, password=None, code=None):
    """Performs authentication with GitHub and returns the instance. Note all
    fields are optional, however if two-factor authentication is enabled on the
    account, code must be specified.
    """
    if username is not None and password is not None:
        print(' (auth given as {}:{})'.format(username, '*'*len(password)))

    def _2fa_func():
        return code

    if code:
        return login(username, password, two_factor_callback=_2fa_func)
    else:
        return GitHub(username, password)

def import_from_github(repo_owner, repo_name, **kwargs):
    print('Will import from \'{}/{}\''.format(repo_owner, repo_name))
    gh = authenticate_with_github(**kwargs)
    print('{} remaining API accesses before rate-limited'.format(gh.ratelimit_remaining))

    issues = list(gh.issues_on(repo_owner, repo_name, state='all'))
    for issue in issues:
        d = issue.as_dict()
        imported_key = d['html_url']

        # Parse tags
        tags = labels_list(d)
        if issue.is_closed():
            tags.append('closed')

        # Don't update existing tickets
        existing_tickets = Ticket.objects.filter(imported_key=imported_key).count()
        if existing_tickets > 0:
            print('TODO: Found {} existing ticket(s) for {}, not updating'.format(existing_tickets, imported_key))
            continue

        # Parse the remaining fields
        user = get_user(d['user']['login'])
        title = d['title']
        created_at = timestamp_to_local(d['created_at'])
        edited_at = timestamp_to_local(d['updated_at'])
        first_comment = html2text(d['body_html'])

        # Create the ticket, tags and first comment
        t = Ticket(title=title, created_at=created_at, edited_at=edited_at, 
                requester=user, imported_key=imported_key)
        t.save()
        t.add_tags(tags)
        c = Comment(raw_text=first_comment, commenter=user)
        t.comment_set.add(c)

        # Add remaining comments
        for comment in issue.comments():
            d = comment.as_dict()
            c = Comment(raw_text=html2text(d['body_html']), commenter=get_user(d['user']['login']),
                    created_at=d['created_at'], edited_at=d['updated_at'])
            t.comment_set.add(c)

        print('Added ticket {} with {} comments'.format(repr(t), t.comment_set.count()))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repo_owner', metavar='REPO_OWNER', 
            help='The repository owner, e.g. sjkingo')
    parser.add_argument('repo_name', metavar='REPO_NAME',
            help='The repository name, e.g. ticketus')
    parser.add_argument('--username',
            help='(optional) The username if the repository is private')
    parser.add_argument('--password',
            help='(optional) The password if the repository is private')
    parser.add_argument('--2fa', action='store_true', dest='needs_2fa_code',
            help='(optional) Prompt for a 2FA code if your account requires it')

    args = parser.parse_args()
    code = None
    if args.needs_2fa_code:
        code = input('--2fa given, please enter your 2FA code (it will not be saved): ')
    import_from_github(args.repo_owner, args.repo_name, username=args.username, password=args.password, code=code)
