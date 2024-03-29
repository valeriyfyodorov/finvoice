# Generated by Django 2.2.5 on 2020-02-26 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0026_auto_20200225_1734'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deal',
            options={'ordering': ('-completed_date', 'name')},
        ),
        migrations.AddField(
            model_name='invoice',
            name='is_reissued',
            field=models.BooleanField(default=True),
        ),
    ]
