from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

from mistune import markdown

class Ticket(models.Model):
    requester = models.ForeignKey(User)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = verbose_name + 's'

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

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket)
    commenter = models.ForeignKey(User)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    raw_text = models.TextField()

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = verbose_name + 's'
        ordering = ['created_datetime']

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
