# Generated by Django 3.1.1 on 2021-10-13 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0078_auto_20210826_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='url',
            field=models.TextField(blank=True, null=True),
        ),
    ]
