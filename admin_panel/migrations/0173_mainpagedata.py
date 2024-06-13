# Generated by Django 3.2.1 on 2024-04-26 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0172_menu_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainPageData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('video_url', models.URLField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Main Page Data',
                'verbose_name_plural': 'Main Page Data',
            },
        ),
    ]
