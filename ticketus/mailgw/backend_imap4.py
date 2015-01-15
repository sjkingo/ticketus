from dateutil.parser import parse as dateutil_parse
from django.conf import settings
import email
import imapclient

from ticketus.mailgw.utils import clean_email_body, add_ticket_from_email

import logging
logger = logging.getLogger('ticketus_mailgw')

def connect_to_server():
    """
    Connects to the IMAP server specified in Django's settings and returns
    the connection object.
    """

    c = imapclient.IMAPClient(settings.TICKETUS_MAILGW_HOST, 
                             port=getattr(settings, 'TICKETUS_MAILGW_PORT', None),
                             use_uid=False,
                             ssl=getattr(settings, 'TICKETUS_MAILGW_SSL', False))
    c.login(settings.TICKETUS_MAILGW_USER, settings.TICKETUS_MAILGW_PASSWD)
    c.select_folder(getattr(settings, 'TICKETUS_MAILGW_FOLDER', 'INBOX'))
    return c

def parse_imap4_email(raw_msg):
    """
    Parses a raw email message (as a bytestring) and returns a tuple of
    (headers, body_text).
    """

    msg = email.message_from_bytes(raw_msg)
    headers = dict(msg.items())
    headers['Date'] = dateutil_parse(headers['Date'])
    body = None
    for part in msg.walk():
        if part.get_content_type() == 'text/plain':
            body = clean_email_body(part.get_payload())
            break
    return (headers, body)

def handle_messages(connection, msg_ids):
    """
    Given a list of message IDs, fetch and parse them and add to the
    database.
    """

    if len(msg_ids) == 0:
        return

    dd = connection.fetch(msg_ids, ['INTERNALDATE', 'RFC822'])
    for session_id, data in dd.items():
        headers, body = parse_imap4_email(data.get(b'RFC822'))
        msgid = headers.get('Message-ID')

        # New message: import as a ticket
        t = add_ticket_from_email(msgid, headers.get('From'), headers.get('Date'), headers.get('Subject'), body)
        if t:
            logger.debug('Added new ticket {} from message {}'.format(t, msgid))
        else:
            logger.debug('Skipped existing message {}'.format(msgid))

    # Mark imported messages as deleted
    connection.delete_messages(msg_ids)

def main():
    c = connect_to_server()
    msgs = c.search(['NOT DELETED'])
    handle_messages(c, msgs)
    c.logout()
