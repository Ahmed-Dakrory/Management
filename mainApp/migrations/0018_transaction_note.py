# Generated by Django 3.2.15 on 2022-10-03 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0017_transaction_type_of_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='note',
            field=models.TextField(blank=True, default=None),
        ),
    ]
