# Generated by Django 3.2.15 on 2022-09-17 18:55

from django.db import migrations, models
import django.db.models.deletion
import mainApp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='attachmentTranscript',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=mainApp.models.path_and_renameListing, verbose_name='ListDoc')),
                ('postDate', models.DateTimeField(auto_now_add=True, null=True)),
                ('content_type', models.CharField(default=None, max_length=500, null=True)),
                ('name', models.TextField(default=None)),
                ('table_name', models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={
                'db_table': 'attachmenttranscript',
            },
        ),
        migrations.CreateModel(
            name='factory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=500)),
                ('name_en', models.CharField(default=None, max_length=500)),
                ('head_phone', models.CharField(default=None, max_length=500)),
                ('factory_phone', models.CharField(default=None, max_length=500)),
                ('tax_number', models.CharField(default=None, max_length=500)),
                ('address', models.TextField(default=None, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_date', models.DateTimeField(blank=True, null=True)),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='mainApp.attachmenttranscript')),
            ],
            options={
                'db_table': 'factory',
            },
        ),
        migrations.CreateModel(
            name='company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=500)),
                ('name_en', models.CharField(default=None, max_length=500)),
                ('head_phone', models.CharField(default=None, max_length=500)),
                ('company_phone', models.CharField(default=None, max_length=500)),
                ('tax_number', models.CharField(default=None, max_length=500)),
                ('address', models.TextField(default=None, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_date', models.DateTimeField(blank=True, null=True)),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='mainApp.attachmenttranscript')),
            ],
            options={
                'db_table': 'company',
            },
        ),
    ]
