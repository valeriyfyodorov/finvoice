# Generated by Django 2.2.5 on 2019-11-18 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0010_auto_20191115_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankrecord',
            name='bank_ref',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
    ]