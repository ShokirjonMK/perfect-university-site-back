# Generated by Django 3.1.1 on 2022-12-22 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0120_externalsection'),
    ]

    operations = [
        migrations.AddField(
            model_name='externalsection',
            name='content_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='externalsection',
            name='content_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='externalsection',
            name='content_sr',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='externalsection',
            name='content_uz',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='externalsection',
            name='title_en',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='externalsection',
            name='title_ru',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='externalsection',
            name='title_sr',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='externalsection',
            name='title_uz',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
