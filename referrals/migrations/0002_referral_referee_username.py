# Generated by Django 3.2.6 on 2021-08-18 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referrals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='referral',
            name='referee_username',
            field=models.CharField(default='None', max_length=20),
        ),
    ]
