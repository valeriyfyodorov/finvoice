# Generated by Django 2.2.5 on 2019-12-13 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webparse', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quoteindication',
            options={'ordering': ('-updated_at', '-created_at')},
        ),
        migrations.AddField(
            model_name='quoteindication',
            name='price_last',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name='quoteindication',
            name='price_previous',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=12),
        ),
    ]
