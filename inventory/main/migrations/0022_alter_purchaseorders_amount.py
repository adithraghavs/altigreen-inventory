# Generated by Django 4.1.1 on 2023-03-02 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_alter_purchaseorders_purchase_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorders',
            name='amount',
            field=models.IntegerField(null=True, verbose_name='Quantity'),
        ),
    ]
