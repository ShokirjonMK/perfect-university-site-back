# Generated by Django 3.1.1 on 2021-06-30 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0060_auto_20210626_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='videogallery',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
