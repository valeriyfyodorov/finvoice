# Generated by Django 2.2.5 on 2019-11-19 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0011_bankrecord_bank_ref'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccount',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
