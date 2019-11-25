# Generated by Django 2.2.5 on 2019-11-25 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0018_auto_20191124_1042'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='companies', to='invoices.Department'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='invoiceAmounCommaCharacter',
            field=models.CharField(blank=True, default='', max_length=3),
        ),
        migrations.AddField(
            model_name='company',
            name='invoiceAmountSignalString1',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='company',
            name='invoiceAmountSignalString2',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='company',
            name='invoiceAmountSkipCharacters',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='company',
            name='invoiceAmountStringLength',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='company',
            name='invoiceDateSignalString1',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='company',
            name='invoiceDateSignalString2',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='company',
            name='invoiceDateSkipCharacters',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='company',
            name='invoiceDateStringFormat',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AddField(
            model_name='company',
            name='invoiceDateStringLength',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='company',
            name='invoiceNumberSignalString1',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='company',
            name='invoiceNumberSignalString2',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='company',
            name='invoiceNumberSkipCharacters',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='company',
            name='invoiceNumberStringLength',
            field=models.IntegerField(default=0),
        ),
    ]