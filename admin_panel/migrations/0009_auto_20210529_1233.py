# Generated by Django 3.1.1 on 2021-05-29 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0008_auto_20210529_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admission',
            name='certificate',
            field=models.SmallIntegerField(choices=[(0, 'Others'), (1, 'Certificate'), (2, 'Academic lyceum diploma'), (3, 'Secondary specialized and vocational College diploma')]),
        ),
    ]
