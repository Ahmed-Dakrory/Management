# Generated by Django 3.2.15 on 2022-09-27 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0012_auto_20220927_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='higher_count',
            field=models.IntegerField(default=True),
        ),
    ]
