# Generated by Django 3.2.15 on 2022-09-17 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='permissionGeneral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=500)),
                ('nameEn', models.CharField(default=None, max_length=500, null=True)),
                ('number', models.IntegerField(default=0)),
                ('mainNameEn', models.CharField(default=None, max_length=500, null=True)),
                ('mainNameAr', models.CharField(default=None, max_length=500, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'permissionGeneral',
            },
        ),
        migrations.CreateModel(
            name='role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=500)),
                ('name_en', models.CharField(default=None, max_length=500)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
                ('permissionGeneral', models.ManyToManyField(to='userApp.permissionGeneral')),
            ],
            options={
                'db_table': 'role',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(blank=True, max_length=100, null=True)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=255, verbose_name='email address')),
                ('approved', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('phone', models.CharField(blank=True, max_length=40, null=True)),
                ('address', models.TextField(default=None, null=True)),
                ('id_number', models.TextField(default=None, null=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='userApp.role')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
