# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('gaoyicrm', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='customer_mobile',
            new_name='mobile',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='investor_name',
            new_name='username',
        ),
        migrations.AddField(
            model_name='client',
            name='password',
            field=models.CharField(default=datetime.datetime(2018, 1, 16, 8, 17, 31, 539852, tzinfo=utc), max_length=32, verbose_name=b'\xe5\xaf\x86\xe7\xa0\x81'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='client',
            name='risk_type',
            field=models.CharField(max_length=32, null=True, verbose_name=b'\xe5\xae\xa2\xe6\x88\xb7\xe6\x9c\x80\xe6\x96\xb0\xe7\x9a\x84\xe9\xa3\x8e\xe9\x99\xa9\xe9\x97\xae\xe5\x8d\xb7\xe6\xb5\x8b\xe8\xaf\x84\xe5\x88\x86\xe6\x95\xb0', blank=True),
        ),
    ]
