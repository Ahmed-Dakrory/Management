# Generated by Django 3.2.15 on 2022-10-14 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0018_transaction_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='mainApp.attachmenttranscript'),
        ),
    ]
