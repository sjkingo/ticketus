# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['created_datetime'], 'verbose_name_plural': 'Comments', 'verbose_name': 'Comment'},
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='text',
            new_name='raw_text',
        ),
    ]
