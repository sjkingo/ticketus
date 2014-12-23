#!/usr/bin/env python

import pathfix

def main():
    from ticketus.core.models import Ticket, Comment
    Comment.objects.all().delete()
    Ticket.objects.all().delete()

if __name__ == '__main__':
    main()
