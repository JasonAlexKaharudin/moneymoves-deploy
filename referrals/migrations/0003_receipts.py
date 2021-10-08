# Generated by Django 3.2.6 on 2021-10-08 05:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('referrals', '0002_referral_products'),
    ]

    operations = [
        migrations.CreateModel(
            name='receipts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referee_phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, unique=True)),
                ('referee', models.CharField(default='None', max_length=150)),
                ('receipt_img', models.ImageField(upload_to='')),
                ('referer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='RefererReceipts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]