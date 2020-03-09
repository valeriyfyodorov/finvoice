# Generated by Django 2.2.5 on 2020-03-09 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0030_auto_20200227_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='total_to_pay',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='template',
            name='is_advance',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='template',
            name='is_reissued',
            field=models.BooleanField(default=True),
        ),
    ]
