# Generated by Django 3.1.1 on 2022-12-10 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0111_auto_20221206_1536'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='departmentinfo',
            options={'ordering': ['order', 'created_at']},
        ),
    ]
