# Generated by Django 3.2.6 on 2021-09-10 06:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referrals', '0018_alter_referral_referee_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orphanlist',
            name='orderRef_obj',
        ),
    ]