# Generated by Django 2.2.5 on 2020-03-10 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0031_auto_20200309_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='is_credit',
            field=models.BooleanField(default=False),
        ),
    ]
