# Generated by Django 3.2.15 on 2022-10-21 23:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainApp', '0021_remove_transaction_factory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommended_number',
            name='category',
        ),
        migrations.CreateModel(
            name='tranche',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=500)),
                ('name_en', models.CharField(default=None, max_length=500)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_date', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_tranche_delete', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_tranche_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tranche',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='tranche',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='mainApp.tranche'),
        ),
        migrations.AddField(
            model_name='recommended_number',
            name='tranche',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='mainApp.tranche'),
        ),
    ]
