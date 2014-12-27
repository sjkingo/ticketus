# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20141227_1729'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['created_at'], 'verbose_name_plural': 'Comments', 'verbose_name': 'Comment'},
        ),
        migrations.AlterModelOptions(
            name='ticket',
            options={'ordering': ['-created_at', 'title'], 'verbose_name_plural': 'Tickets', 'verbose_name': 'Ticket'},
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='created_datetime',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='created_datetime',
            new_name='created_at',
        ),
    ]
