# Generated by Django 4.1.1 on 2023-02-10 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_invoicemaster_delivery_challan'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoicemaster',
            name='delivery_challan_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
