# Generated by Django 3.2.6 on 2021-09-21 20:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210922_0335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='webhookorder',
            name='discount_code',
        ),
    ]
