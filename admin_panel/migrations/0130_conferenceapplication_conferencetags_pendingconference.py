# Generated by Django 3.1.1 on 2023-05-16 17:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0129_auto_20230419_1709'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConferenceTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Conference Tag',
                'verbose_name_plural': 'Conference Tags',
                'db_table': 'conference_tags',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='PendingConference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('date', models.DateField(verbose_name='Date')),
                ('time', models.CharField(max_length=20, verbose_name='Time')),
                ('description', models.TextField(verbose_name='Description')),
                ('image', models.ImageField(upload_to='conference', verbose_name='Image')),
                ('views', models.IntegerField(default=0, verbose_name='Views')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('tags', models.ManyToManyField(to='admin_panel.ConferenceTags', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Pending Conference',
                'verbose_name_plural': 'Pending Conferences',
                'db_table': 'pending_conference',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ConferenceApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, verbose_name='Full Name')),
                ('phone_number', models.CharField(max_length=255, verbose_name='Phone Number')),
                ('addition_phone_number', models.CharField(blank=True, max_length=255, verbose_name='Addition Phone Number')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('file', models.FileField(upload_to='conference_application', verbose_name='File')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.pendingconference', verbose_name='Conference')),
            ],
            options={
                'verbose_name': 'Conference Application',
                'verbose_name_plural': 'Conference Applications',
                'db_table': 'conference_application',
                'ordering': ['-id'],
            },
        ),
    ]
