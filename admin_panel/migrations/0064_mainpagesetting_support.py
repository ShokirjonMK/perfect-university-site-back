# Generated by Django 3.1.1 on 2021-07-05 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0063_auto_20210703_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpagesetting',
            name='support',
            field=models.URLField(blank=True, null=True, verbose_name='Universitetni boshqarishlab-quvvatlash'),
        ),
    ]
