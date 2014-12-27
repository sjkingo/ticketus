# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20141227_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='imported_key',
            field=models.CharField(max_length=255, unique=True, blank=True),
            preserve_default=True,
        ),
    ]
