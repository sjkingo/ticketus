import email
from email_reply_parser import EmailReplyParser

from ticketus.core.models import Ticket, Comment
from ticketus.core.utils import get_user

def clean_email_body(raw_body):
    """
    Cleans an email's plain text body by stripping out any signatures.
    """
    s = EmailReplyParser.read(raw_body)
    return r'\n'.join([f.content for f in s.fragments if not f.signature])

def get_user_from_sender(from_header):
    """
    Gets (or creates) the Django User when given a From: header in the format:

    Name <email>
    """
    from_name, from_email = email.utils.parseaddr(from_header)
    from_username = from_email.split('@')[0]
    user = get_user(from_username, defaults={
        'first_name': from_name.split(' ')[0],
        'last_name': ' '.join(from_name.split(' ')[1:]),
        'email': from_email,
    })
    return user

def add_ticket_from_email(msgid, from_header, created_at, subject, body):
    """
    Adds a new ticket to the database.
    """

    msgid = 'mailgw:' + msgid

    # First, check the imported_key for any existing messages matching
    # this Message-ID. This prevents duplicates from being added.
    if Ticket.objects.filter(imported_key=msgid).count() != 0:
        return None

    # Add to database
    user = get_user_from_sender(from_header)
    t = Ticket(title=subject, created_at=created_at, requester=user, imported_key=msgid)
    t.save()
    c = Comment(raw_text=body, commenter=user)
    t.comment_set.add(c)
    return t
