# Generated by Django 3.2.15 on 2022-10-03 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0015_recommended_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommended_number',
            name='number',
            field=models.IntegerField(blank=True, default=None),
        ),
    ]