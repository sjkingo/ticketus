# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20141228_0651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='imported_key',
            field=models.CharField(blank=True, null=True, max_length=255, unique=True),
            preserve_default=True,
        ),
    ]
