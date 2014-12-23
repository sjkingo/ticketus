from django.db import models

from ticketus.core.models import *

class Tag(models.Model):
    ticket = models.ForeignKey(Ticket)
    tag_name = models.CharField(max_length=50)
    added_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = verbose_name + 's'
        unique_together = ('ticket', 'tag_name')
        ordering = ['added_datetime']

    def __str__(self):
        return self.tag_name

    def __repr__(self):
        return '<Tag \'{}\' for {}'.format(self.tag_name, self.ticket)

