# Generated by Django 4.1.1 on 2023-03-02 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_delete_equipmentsubcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorders',
            name='purchase_order_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]