# Generated by Django 3.2.6 on 2021-08-18 07:38

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_num_of_refers'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrphanList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Phone_Number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('wallet', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
            ],
        ),
    ]
