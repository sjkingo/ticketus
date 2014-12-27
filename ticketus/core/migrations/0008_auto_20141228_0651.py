# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20141228_0646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='edited_at',
            field=models.DateTimeField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='edited_at',
            field=models.DateTimeField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
