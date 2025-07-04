# Generated by Django 5.1.7 on 2025-03-12 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0021_alter_companyimage_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Traveller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('user_id', models.CharField(max_length=50, unique=True)),
                ('package_choice', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Pending', 'Pending')], max_length=50)),
                ('tour_type', models.CharField(choices=[('Solo', 'Solo'), ('Group', 'Group')], max_length=50)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('date_of_tour', models.DateField()),
            ],
        ),
    ]
