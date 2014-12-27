# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20141223_1827'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticket',
            options={'verbose_name_plural': 'Tickets', 'ordering': ['-created_datetime', 'title'], 'verbose_name': 'Ticket'},
        ),
        migrations.AddField(
            model_name='ticket',
            name='imported_key',
            field=models.CharField(max_length=255, blank=True, default=''),
            preserve_default=False,
        ),
    ]
