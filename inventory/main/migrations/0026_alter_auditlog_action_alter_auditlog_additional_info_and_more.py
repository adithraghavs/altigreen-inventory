# Generated by Django 4.1.1 on 2023-04-23 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_auditlog_action_auditlog_additional_info_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auditlog',
            name='action',
            field=models.CharField(blank=True, editable=False, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='auditlog',
            name='additional_info',
            field=models.TextField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='auditlog',
            name='subject',
            field=models.CharField(blank=True, editable=False, max_length=1000, null=True),
        ),
    ]
