#!/usr/bin/env python

"""IMAP4 mail gateway for Ticketus.

The following settings can be used to configure this program:

    TICKETUS_MAILGW_HOST:    Required. Hostname to connect to.
    TICKETUS_MAILGW_PORT:    Optional. Override the default port (default: 143 for IMAP, 993 for IMAPS)
    TICKETUS_MAILGW_SSL:     Optional. Use SSL/TLS to connect (changes port to 993 unless overridden). 
                               Defaults to False
    TICKETUS_MAILGW_USER:    Required. Username to authenticate with.
    TICKETUS_MAILGW_PASSWD:  Required. Password to authenticate with.
    TICKETUS_MAILGW_FOLDER:  Optional. The IMAP folder to fetch messages from (default: 'INBOX')

"""

import os.path, sys
sys.path.append(os.path.realpath('..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticketus.settings')
import django
django.setup()

from ticketus.mailgw.backend_imap4 import main
main()
