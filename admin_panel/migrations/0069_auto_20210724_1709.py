# Generated by Django 3.1.1 on 2021-07-24 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0068_remove_menu_only_footer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usefullink',
            options={'ordering': ['order'], 'verbose_name': 'Hamkor', 'verbose_name_plural': 'Hamkorlar'},
        ),
    ]
