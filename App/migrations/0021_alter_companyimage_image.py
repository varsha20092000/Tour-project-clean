# Generated by Django 3.2.25 on 2025-03-10 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0020_companyimage_companyprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyimage',
            name='image',
            field=models.ImageField(upload_to='static/images/'),
        ),
    ]
