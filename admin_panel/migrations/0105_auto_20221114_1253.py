# Generated by Django 3.1.1 on 2022-11-14 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0104_auto_20221114_1117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='internationalconferencepage',
            name='conferences',
        ),
        migrations.AddField(
            model_name='internationalconferencepage',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='internationalconferencepage',
            name='title_en',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='internationalconferencepage',
            name='title_ru',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='internationalconferencepage',
            name='title_sr',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='internationalconferencepage',
            name='title_uz',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
