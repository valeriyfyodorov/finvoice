# Generated by Django 2.2.5 on 2019-11-20 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0013_template_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='bank_records',
        ),
        migrations.AddField(
            model_name='bankrecord',
            name='invoices',
            field=models.ManyToManyField(blank=True, related_name='bank_records', to='invoices.Invoice'),
        ),
    ]
