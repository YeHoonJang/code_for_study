# Generated by Django 2.1 on 2018-08-23 08:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('relocations', '0008_auto_20180823_1605'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default='')),
                ('file', models.FileField(null=True, upload_to='')),
            ],
        ),
        migrations.AlterField(
            model_name='contents',
            name='upload_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 23, 8, 40, 45, 961576, tzinfo=utc), verbose_name='upload date'),
        ),
    ]
