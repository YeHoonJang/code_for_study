# Generated by Django 2.1 on 2018-08-23 07:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('relocations', '0007_auto_20180821_1604'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contents',
            old_name='content_author',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='contents',
            old_name='content_file',
            new_name='file',
        ),
        migrations.RenameField(
            model_name='contents',
            old_name='content_name',
            new_name='title',
        ),
        migrations.AlterField(
            model_name='contents',
            name='upload_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 23, 7, 5, 35, 335437, tzinfo=utc), verbose_name='upload date'),
        ),
    ]
