# Generated by Django 3.1.1 on 2022-11-10 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0099_auto_20221109_1110'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScientificJournal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Kiritilgan sana')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan sana")),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('title_uz', models.CharField(max_length=255, null=True, verbose_name='title')),
                ('title_sr', models.CharField(max_length=255, null=True, verbose_name='title')),
                ('title_en', models.CharField(max_length=255, null=True, verbose_name='title')),
                ('title_ru', models.CharField(max_length=255, null=True, verbose_name='title')),
                ('file', models.FileField(upload_to='scientific-file')),
                ('image', models.ImageField(upload_to='scientific')),
            ],
            options={
                'verbose_name': 'Scientific Journal',
                'verbose_name_plural': 'Scientific Journals',
                'db_table': 'scientific_journal',
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='ScientificJournalDesc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Kiritilgan sana')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan sana")),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('title_uz', models.CharField(max_length=255, null=True, verbose_name='Title')),
                ('title_sr', models.CharField(max_length=255, null=True, verbose_name='Title')),
                ('title_en', models.CharField(max_length=255, null=True, verbose_name='Title')),
                ('title_ru', models.CharField(max_length=255, null=True, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('description_uz', models.TextField(null=True, verbose_name='Description')),
                ('description_sr', models.TextField(null=True, verbose_name='Description')),
                ('description_en', models.TextField(null=True, verbose_name='Description')),
                ('description_ru', models.TextField(null=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Scientific Journal Desc',
                'ordering': ('created_at',),
            },
        ),
    ]
