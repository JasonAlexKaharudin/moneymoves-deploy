# Generated by Django 3.2.4 on 2021-06-27 11:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('merchants', '0002_merchant_date_joined'),
    ]

    operations = [
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referer_cashback', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('referee_cashback', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('receipt', models.ImageField(default='default.jpg', upload_to='receipts')),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='merchants.merchant')),
                ('referee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referee', to=settings.AUTH_USER_MODEL)),
                ('referer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
