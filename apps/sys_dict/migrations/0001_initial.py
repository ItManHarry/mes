# Generated by Django 4.2.1 on 2024-05-21 06:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SysDict',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('created_by', models.IntegerField(null=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_by', models.IntegerField(null=True)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=8, unique=True)),
            ],
            options={
                'db_table': 'sys_dict',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SysEnum',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('created_by', models.IntegerField(null=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_by', models.IntegerField(null=True)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=4)),
                ('sys_dict', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sys_dict.sysdict')),
            ],
            options={
                'db_table': 'sys_enum',
                'abstract': False,
            },
        ),
    ]
