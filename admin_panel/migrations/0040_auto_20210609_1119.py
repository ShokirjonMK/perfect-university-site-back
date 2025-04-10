# Generated by Django 3.1.1 on 2021-06-09 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0039_auto_20210609_1111'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service',
            old_name='white_icon',
            new_name='main_icon',
        ),
        migrations.AlterField(
            model_name='admission',
            name='certificate',
            field=models.SmallIntegerField(choices=[(3, 'Secondary specialized and vocational College diploma'), (2, 'Academic lyceum diploma'), (1, 'Certificate'), (0, 'Others')]),
        ),
    ]
