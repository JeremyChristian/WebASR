# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0002_upload_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='system',
            name='command',
            field=models.CharField(default='string', max_length=200),
            preserve_default=False,
        ),
    ]
