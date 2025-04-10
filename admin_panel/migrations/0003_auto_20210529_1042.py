# Generated by Django 3.1.1 on 2021-05-29 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0002_auto_20210529_0307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admission',
            name='certificate',
            field=models.SmallIntegerField(choices=[(2, 'Academic lyceum diploma'), (0, 'Others'), (3, 'Secondary specialized and vocational College diploma'), (1, 'Certificate')]),
        ),
        migrations.AlterField(
            model_name='admission',
            name='language_qualifications',
            field=models.SmallIntegerField(choices=[(0, 'English'), (1, 'German'), (2, 'French'), (3, 'Russian'), (4, 'Others')]),
        ),
    ]
