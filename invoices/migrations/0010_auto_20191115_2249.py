# Generated by Django 2.2.5 on 2019-11-15 22:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0009_auto_20191115_2228'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invoice',
            options={'ordering': ('-issued_date',)},
        ),
    ]
