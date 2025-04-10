# Generated by Django 3.2.1 on 2023-11-09 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0144_news_objectives'),
    ]

    operations = [
        migrations.CreateModel(
            name='OurMission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Title')),
                ('description', models.TextField(null=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Our Mission',
                'verbose_name_plural': 'Our Missions',
            },
        ),
    ]
