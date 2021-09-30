from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from merchants.models import Partner_Merchant
import api.models
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from webapp import settings

import decimal

# Create your models here.
class Referral(models.Model):
    referer_username = models.ForeignKey(User, on_delete=CASCADE, related_name="referer", null=True)
    merchant = models.ForeignKey(Partner_Merchant ,on_delete=CASCADE, null=True)
    sessionID = models.IntegerField(default=0)
    orderID = models.CharField(max_length=20, default=0)  
    totalAmt = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    referer_cashback = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    referee_cashback = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    referee_email = models.EmailField(max_length=50, default="None")
    referee_username = models.CharField(max_length=40, default="Not Signed Up")
    is_Verified = models.BooleanField(default=False)
    stored_in_wallet = models.BooleanField(default=False)
    referee_has_account = models.BooleanField(default=False)
    orderRef_obj = models.OneToOneField(api.models.orderRef, on_delete=CASCADE, null=True, default=None)
    date_published = models.DateTimeField(default=datetime.now, blank=True)

    def get_absolute_url(self):
        return reverse('referrals:referral-list')

    def __str__(self):
        return f"{self.merchant.name} {self.orderID}. Referred by: {self.referer_username.username}"

class OrphanList(models.Model):
    refereeEmail = models.EmailField(max_length=40, default=0)
    referee_cashback = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    referral_obj = models.OneToOneField(Referral, on_delete=CASCADE, default=None, null=True)

    def __str__(self):
        return f"{self.merchant.name} {self.orderID}. Referred by: {self.referer_username.username}"   


@receiver(post_save, sender=Referral)
def post_save_Referral(sender, instance, created, *args, **kwargs):
    if created:
        if instance.referer_username.email == instance.referee_email:
            pass
        else:
            # sunday valley has 30% cashback: 15% each 
            if instance.merchant.name == "Sunday-Valley":
                instance.referer_cashback = round(decimal.Decimal(instance.totalAmt) * decimal.Decimal(0.15), 2)
                instance.referee_cashback = round(decimal.Decimal(instance.totalAmt) * decimal.Decimal(0.15), 2)
                instance.save()
            if instance.merchant.name == "Singaplex":
                instance.referer_cashback = round(decimal.Decimal(instance.totalAmt) * decimal.Decimal(0.075), 2)
                instance.referee_cashback = round(decimal.Decimal(instance.totalAmt) * decimal.Decimal(0.075), 2)
                instance.save()
            if instance.merchant.name == "Do-Not-Cross":
                instance.referer_cashback = round(decimal.Decimal(instance.totalAmt) * decimal.Decimal(0.15), 2)
                instance.referee_cashback = round(decimal.Decimal(instance.totalAmt) * decimal.Decimal(0.15), 2)
                instance.save()
            if instance.merchant.name == "Jemaime":
                instance.referer_cashback = round(decimal.Decimal(instance.totalAmt) * decimal.Decimal(0.05), 2)
                instance.referee_cashback = round(decimal.Decimal(instance.totalAmt) * decimal.Decimal(0.05), 2)
                instance.save()

            #update referrer cashback
            referer = instance.referer_username
            referer.profile.wallet = referer.profile.wallet + instance.referer_cashback
            referer.profile.num_of_refers = referer.profile.num_of_refers + 1
            referer.profile.save()

            #send email to referrer
            subject = 'Successful Referral!'
            html_message = render_to_string('referrals/success-referral.html', {
                'referer': referer, 
                'wallet': instance.referer_cashback, 
                'referee': instance.referee_email
            })
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            to = referer.email
            mail.send_mail(subject, plain_message, from_email,[to], html_message = html_message)
            

        #check the if refereeEmail has an account 
        #if exist, then update wallet of referee, 
        #if dne, then send email to them and populate orphan list
        if User.objects.filter(email=instance.referee_email).exists():
            referee = User.objects.filter(email=instance.referee_email)[0]
            referee.profile.wallet = referee.profile.wallet + instance.referee_cashback
            referee.profile.num_of_refers = referee.profile.num_of_refers + 1
            referee.profile.save()

            instance.referee_username = referee.username
            instance.referee_has_account = True
            instance.save()

            #send email to referee with an account
            subject = 'Successful Purchase!'
            html_message = render_to_string('referrals/success-referee.html', {
                'referee': referee,
                'referer': instance.referer_username.username, 
                'cashback': instance.referee_cashback
            })
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            to = instance.referee_email
            mail.send_mail(subject, plain_message, from_email,[to], html_message = html_message)

        else:
            newOrphan = OrphanList.objects.create(
                refereeEmail = instance.referee_email,
                referee_cashback = instance.referee_cashback,
                referral_obj = instance
            )
            newOrphan.save()
            subject = 'Successful Purchase!'
            html_message = render_to_string('referrals/success-referee-no-acc.html', {
                'referer': instance.referer_username.username, 
                'cashback': instance.referee_cashback
            })
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            to = instance.referee_email
            mail.send_mail(subject, plain_message, from_email,[to], html_message = html_message)