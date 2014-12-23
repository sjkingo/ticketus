from django.contrib.auth.models import User
from django.db import models

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

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket)
    commenter = models.ForeignKey(User)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    text = models.TextField()

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = verbose_name + 's'
        ordering = ['created_datetime']

    def __str__(self):
        return 'Comment for ' + repr(self.ticket)

    def __repr__(self):
        return '<{}>'.format(str(self))
