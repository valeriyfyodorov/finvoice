# Generated by Django 2.2.5 on 2019-12-14 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webparse', '0002_auto_20191213_1923'),
    ]

    operations = [
        migrations.CreateModel(
            name='SymbolCommodity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix', models.CharField(max_length=4)),
                ('name', models.CharField(max_length=4)),
            ],
            options={
                'ordering': ('prefix',),
            },
        ),
        migrations.CreateModel(
            name='SymbolPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suffix', models.CharField(max_length=4)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ('suffix',),
            },
        ),
        migrations.AddField(
            model_name='quoteindication',
            name='price_change',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=12),
        ),
    ]
