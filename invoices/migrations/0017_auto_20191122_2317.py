# Generated by Django 2.2.5 on 2019-11-22 23:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0016_auto_20191121_0859'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invoice',
            options={'ordering': ('-number', '-issued_date')},
        ),
    ]
