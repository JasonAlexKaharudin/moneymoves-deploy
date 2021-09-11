# Generated by Django 3.2.6 on 2021-09-11 06:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0015_auto_20210910_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderref',
            name='merchant_name',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='merchants.merchant'),
        ),
        migrations.AlterField(
            model_name='orderref',
            name='referrer',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]