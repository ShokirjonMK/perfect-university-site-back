# Generated by Django 3.1.1 on 2021-05-29 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0013_auto_20210529_1443'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Council',
        ),
        migrations.AlterField(
            model_name='admission',
            name='certificate',
            field=models.SmallIntegerField(choices=[(2, 'Academic lyceum diploma'), (1, 'Certificate'), (0, 'Others'), (3, 'Secondary specialized and vocational College diploma')]),
        ),
    ]
