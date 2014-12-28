#!/usr/bin/env python

"""Import script for Freshdesk (www.freshdesk.com) to Ticketus.

This script requires some added libraries. If they are not installed you will
need to install them first using pip:

 * html2text
 * requests
 * pytz

This is *not* a destructive operation. This script will not delete any existing
tickets; instead each ticket will be created with the `imported_key` field set
to the unique URI given by Freshdesk for each ticket.. This means you do not
need to ensure uniqueness with any existing tickets. Each time the script is
run, new tickets will be added and no duplicates will be created.

You must specify the helpdesk domain and API key as arguments. You may find
your API key by logging in to the Freshdesk portal, clicking the profile
picture in the top right, and going to Profile settings. You will see the API
key listed.

Please note that Freshdesk rate-limits access to the API to 1000 requests/hr.
See http://freshdesk.com/api#ratelimit for more information.
"""

# Import django
import os.path, sys
sys.path.append(os.path.realpath('..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticketus.settings')
import django
django.setup()

import datetime
from html2text import html2text
import requests
from requests.exceptions import HTTPError
import pytz

from django.contrib.auth.models import User
from ticketus.core.models import *

def get_user(username):
    """Given a username, gets or creates it in the local database and returns
    the User instance."""
    user, created = User.objects.get_or_create(username=username)
    return user

def email_to_username(email):
    return email.split('@')[0]

def timestamp_to_datetime(timestamp):
    # 2014-08-08T06:39:00+10:00
    return datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S+10:00')

def execute_api(config, partial_url, page=None):
    # Construct the URL
    full_url = config['url_prefix'] + partial_url + '?format=json'
    if page is not None:
        full_url += '&page={}'.format(page)

    r = requests.get(full_url, auth=(config['api_key'], 'dummy_password_not_used'))
    r.raise_for_status()
    resp = r.json()
    if 'require_login' in resp:
        raise HTTPError('Authentication failed. Either the API key specified is invalid or it does not have authorization to list tickets')
    return resp

def lookup_user_freshdesk(d, user_id):
    u = execute_api(d, '/contacts/{}.json'.format(user_id))
    return email_to_username(u['user']['email'])

def import_from_freshdesk(helpdesk_domain, api_key):
    d = {'url_prefix': 'http://' + helpdesk_domain,
         'api_key': api_key}

    existing_users = {}

    page = 1
    while True:
        # Fetch the current page of tickets and exit if there are no results
        tickets = execute_api(d, '/helpdesk/tickets/filter/all_tickets', page=page)
        if len(tickets) == 0:
            break
        page += 1

        for ticket_overview in tickets:
            ticket = execute_api(d, '/helpdesk/tickets/{}.json'.format(
                    ticket_overview['display_id']))['helpdesk_ticket']

            # Get the requester's information and store it to save API requests
            requester_id = str(ticket['requester_id'])
            if requester_id not in existing_users:
                existing_users[requester_id] = lookup_user_freshdesk(d, requester_id)
            user = get_user(existing_users[requester_id])

            # Extract ticket fields
            title = ticket['subject']
            created_at = timestamp_to_datetime(ticket['created_at'])
            updated_at = timestamp_to_datetime(ticket['updated_at'])
            first_comment = html2text(ticket['description_html'])
            tags = ticket['tags']
            unique_uri = d['url_prefix'] + '/helpdesk/tickets/{}'.format(ticket['display_id'])

            # Closed is represented by a tag
            is_closed = ticket['status_name'] == 'Closed'
            if is_closed:
                tags.append('closed')

            # Create the ticket, tags and first comment
            t = Ticket(title=title, created_at=created_at, edited_at=updated_at, 
                    requester=user, imported_key=unique_uri)
            t.save()
            t.add_tags(tags)
            c = Comment(raw_text=first_comment, commenter=user)
            t.comment_set.add(c)

            # Add any comments
            for note in ticket['notes']:
                comment = note['note']

                if comment['user_id'] not in existing_users:
                    existing_users[comment['user_id']] = lookup_user_freshdesk(d, comment['user_id'])
                comment_user = get_user(existing_users[comment['user_id']])

                comment_created_at = timestamp_to_datetime(comment['created_at'])
                comment_updated_at = timestamp_to_datetime(comment['updated_at'])
                comment_body_text = html2text(comment['body_html'])

                c = Comment(raw_text=comment_body_text, created_at=comment_created_at,
                        edited_at=comment_updated_at, commenter=comment_user)
                t.comment_set.add(c)

            print('Added ticket {} with {} comments'.format(repr(t), t.comment_set.count()))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('helpdesk_domain', metavar='HELPDESK_DOMAIN', 
            help='The domain where the helpdesk is running, e.g. test.freshdesk.com')
    parser.add_argument('api_key', metavar='API_KEY',
            help='Your API key to authenticate')

    args = parser.parse_args()
    import_from_freshdesk(args.helpdesk_domain, args.api_key)
