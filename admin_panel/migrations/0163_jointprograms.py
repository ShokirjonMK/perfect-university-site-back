# Generated by Django 3.2.1 on 2023-11-22 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0162_ranking'),
    ]

    operations = [
        migrations.CreateModel(
            name='JointPrograms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('title_uz', models.CharField(max_length=255, null=True, verbose_name='Title')),
                ('title_sr', models.CharField(max_length=255, null=True, verbose_name='Title')),
                ('title_en', models.CharField(max_length=255, null=True, verbose_name='Title')),
                ('title_ru', models.CharField(max_length=255, null=True, verbose_name='Title')),
                ('image', models.ImageField(upload_to='joint_programs', verbose_name='Image')),
                ('link', models.URLField(verbose_name='Link')),
                ('order', models.IntegerField(verbose_name='Order')),
            ],
            options={
                'verbose_name': 'Joint program',
                'verbose_name_plural': 'Joint programs',
                'ordering': ['order'],
            },
        ),
    ]
