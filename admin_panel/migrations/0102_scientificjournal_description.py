# Generated by Django 3.1.1 on 2022-11-11 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0101_scientificjournal_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='scientificjournal',
            name='description',
            field=models.TextField(null=True, verbose_name='Description'),
        ),
    ]
