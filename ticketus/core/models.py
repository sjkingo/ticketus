from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

import datetime
from mistune import markdown

class TimestampModel(models.Model):
    created_at = models.DateTimeField()
    edited_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Update created and edited timestamps if they are not provided"""
        is_created = self.pk is None
        now = datetime.datetime.now()
        if is_created:
            if not self.created_at:
                self.created_at = now
        else:
            if not self.edited_at:
                self.edited_at = now
        super(TimestampModel, self).save(*args, **kwargs)

class Ticket(TimestampModel):
    requester = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    imported_key = models.CharField(max_length=255, blank=True, null=True, unique=True)

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = verbose_name + 's'
        ordering = ['-created_at', 'title']

    def __str__(self):
        return self.title

    def __repr__(self):
        return '<Ticket \'{}\'>'.format(self.title)

    def get_absolute_url(self):
        return reverse('ticket', args=[self.id])

    def add_tags(self, tag_list):
        """Given a list of tag names, create tags for them."""
        for tag in tag_list:
            if self.tag_set.filter(tag_name=tag).exists():
                continue
            self.tag_set.create(tag_name=tag)

class Comment(TimestampModel):
    ticket = models.ForeignKey(Ticket)
    commenter = models.ForeignKey(User)
    raw_text = models.TextField()

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = verbose_name + 's'
        ordering = ['created_at']

    def __str__(self):
        return 'Comment for ' + repr(self.ticket)

    def __repr__(self):
        return '<{}>'.format(str(self))

    def get_absolute_url(self):
        return self.ticket.get_absolute_url() + '#comment-' + self.id

    @property
    def text(self):
        """Pass the raw_text field through a Markdown parser and return its result."""
        return markdown(self.raw_text)
