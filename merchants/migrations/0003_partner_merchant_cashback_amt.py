# Generated by Django 3.2.6 on 2021-09-23 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0002_auto_20210923_0658'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner_merchant',
            name='cashback_amt',
            field=models.IntegerField(default=0),
        ),
    ]