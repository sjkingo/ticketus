#!/usr/bin/env python

"""Import script for Freshdesk (www.freshdesk.com) to Ticketus.

This script requires some added libraries. If they are not installed you will
need to install them first using pip:

 * html2text
 * python-freshdesk

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

from html2text import html2text

# Check that python-freshdesk is installed
try:
    from freshdesk.api import API
except ImportError:
    print('ERROR: python-freshdesk is not installed. Please run (inside a virtualenv):')
    print('  pip install python-freshdesk')
    exit(1)

from django.contrib.auth.models import User
from ticketus.core.models import *

def get_user(api, requester_id):
    contact = api.contacts.get_contact(requester_id)
    username = contact.email.split('@')[0]
    user, created = User.objects.get_or_create(username=username, defaults={'email': contact.email})
    return user

def import_from_freshdesk(helpdesk_domain, api_key):
    a = API(helpdesk_domain, api_key)

    # Fetch the current page of tickets and exit if there are no results
    tickets = a.tickets.list_all_tickets()
    for ticket in tickets:
        unique_uri = 'http://{}/helpdesk/tickets/{}'.format(helpdesk_domain, ticket.display_id)

        # Don't modify existing tickets
        if Ticket.objects.filter(imported_key=unique_uri).count() != 0:
            continue

        # Create the ticket
        user = get_user(a, str(ticket.requester_id))
        t = Ticket(title=ticket.subject, created_at=ticket.created_at, edited_at=ticket.updated_at, 
                requester=user, imported_key=unique_uri)
        t.save()

        # Add the tags, including ticket status
        t.add_tags(ticket.tags)
        t.add_tags([ticket.status])

        # Add the first comment ("description")
        c = Comment(raw_text=html2text(ticket.description_html), commenter=user)
        t.comment_set.add(c)

        # Add any further comments
        for comment in ticket.comments:
            comment_user = get_user(a, str(comment.user_id))
            c = Comment(raw_text=html2text(comment.body_html), created_at=comment.created_at,
                    edited_at=comment.updated_at, commenter=comment_user)
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
