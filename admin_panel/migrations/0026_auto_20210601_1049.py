# Generated by Django 3.1.1 on 2021-06-01 05:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0025_auto_20210529_1837'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdmissionPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('views', models.IntegerField(default=0)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'admission_page',
                'ordering': ('-publish_date',),
            },
        ),
        migrations.AlterField(
            model_name='admission',
            name='certificate',
            field=models.SmallIntegerField(choices=[(3, 'Secondary specialized and vocational College diploma'), (2, 'Academic lyceum diploma'), (0, 'Others'), (1, 'Certificate')]),
        ),
    ]
