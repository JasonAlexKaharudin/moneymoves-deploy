# Generated by Django 3.2.6 on 2021-08-18 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_rename_wallet_profile_orphan_cashback'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orphanlist',
            old_name='wallet',
            new_name='orphan_cashback',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='orphan_cashback',
            new_name='wallet',
        ),
    ]
