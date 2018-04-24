# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gaoyicrm', '0002_auto_20180116_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='union_id',
            field=models.CharField(default=b'_', max_length=128, null=True, verbose_name=b'\xe5\xbe\xae\xe4\xbf\xa1unionId', blank=True),
        ),
    ]
