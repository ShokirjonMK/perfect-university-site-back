# Generated by Django 3.1.1 on 2021-05-29 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0003_auto_20210529_1042'),
    ]

    operations = [
        migrations.RenameField(
            model_name='admission',
            old_name='errorr_fill',
            new_name='error_fill',
        ),
        migrations.AlterField(
            model_name='admission',
            name='certificate',
            field=models.SmallIntegerField(choices=[(3, 'Secondary specialized and vocational College diploma'), (1, 'Certificate'), (0, 'Others'), (2, 'Academic lyceum diploma')]),
        ),
    ]
