# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20141227_1312'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='modified_datetime',
            new_name='edited_at',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='modified_datetime',
            new_name='edited_at',
        ),
    ]
