# Generated by Django 3.2.1 on 2023-11-10 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0152_auto_20231110_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='facebook',
            field=models.URLField(blank=True, null=True, verbose_name='Facebook'),
        ),
        migrations.AddField(
            model_name='staff',
            name='instagram',
            field=models.URLField(blank=True, null=True, verbose_name='Instagram'),
        ),
        migrations.AddField(
            model_name='staff',
            name='linkedin',
            field=models.URLField(blank=True, null=True, verbose_name='Linkedin'),
        ),
    ]
