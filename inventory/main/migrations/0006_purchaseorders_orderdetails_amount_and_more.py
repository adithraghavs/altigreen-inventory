# Generated by Django 4.1.1 on 2022-10-08 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_equipmentcategory_equipment_master_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseOrders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_order_number', models.IntegerField(blank=True, null=True)),
                ('purchase_order_date', models.CharField(blank=True, max_length=100, null=True)),
                ('amount', models.IntegerField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='amount',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='purchase_order_date',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='equipmentmaster',
            name='equipment_type',
            field=models.CharField(choices=[('0', 'Laptop'), ('1', 'Desktop'), ('2', 'Networking device'), ('3', 'Mouse'), ('4', 'Access Point'), ('5', 'Printer'), ('6', 'Scanner'), ('7', 'CCTV')], max_length=50),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='purchase_order_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]