# Generated by Django 5.1.7 on 2025-03-21 13:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0025_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.user'),
        ),
    ]
