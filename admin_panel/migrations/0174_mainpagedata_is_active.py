# Generated by Django 3.2.1 on 2024-05-01 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0173_mainpagedata'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpagedata',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Default Main Page Active'),
        ),
    ]
