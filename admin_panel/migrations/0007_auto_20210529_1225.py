# Generated by Django 3.1.1 on 2021-05-29 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0006_auto_20210529_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admission',
            name='certificate',
            field=models.SmallIntegerField(choices=[(3, 'Secondary specialized and vocational College diploma'), (1, 'Certificate'), (0, 'Others'), (2, 'Academic lyceum diploma')]),
        ),
        migrations.AlterField(
            model_name='admission',
            name='error_fill',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='admission',
            name='status',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
