# Generated by Django 4.1.1 on 2022-10-25 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_employeemaster_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterinventory',
            name='employee_id',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
