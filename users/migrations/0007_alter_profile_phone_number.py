# Generated by Django 3.2.6 on 2021-08-23 03:55

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20210818_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='Phone_Number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True),
        ),
    ]