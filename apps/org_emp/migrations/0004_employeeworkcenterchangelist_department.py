# Generated by Django 4.2.1 on 2024-05-24 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('org_emp', '0003_rename_emloyeeworkcenterchangelist_employeeworkcenterchangelist'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeworkcenterchangelist',
            name='department',
            field=models.CharField(max_length=512, null=True),
        ),
    ]
