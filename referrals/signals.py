from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Referral, OrphanList
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from webapp import settings

import json
import decimal

def sendEmailHelper(EmailSubject, template, context, to):
    template = render_to_string(template, context)
    message = strip_tags(template)
    mail.send_mail(EmailSubject, message, settings.EMAIL_HOST_USER, [to], html_message=template);

def updateWallet(user, cashback, isReferer):
    user.profile.wallet = user.profile.wallet + cashback
    if isReferer == True:
        user.profile.num_of_refers = user.profile.num_of_refers + 1
    user.profile.save()

def cashbackCalc(cashbackAmt, price, qty):
    return round(decimal.Decimal(price) * decimal.Decimal(cashbackAmt) * decimal.Decimal(qty),2)

def splitCashback(currentCash, newCash):
    return currentCash + round(decimal.Decimal(newCash), 2)

@receiver(post_save, sender=Referral)
def post_save_Referral(sender, instance, created, *args, **kwargs):
    if created:
        if instance.webhook != None and instance.orderRef_obj != None:
            # sunday valley has 30% cashback: 15% each 
            if instance.merchant.name == "Sunday-Valley":
                products = instance.products
                products = json.loads(str(products))

                cashback = 0
                # Parse the Product list 
                for p in products:
                    if p == "The Crown tote bag [King Collection V1]":
                        cashback = cashback + cashbackCalc(0.15, products['The Crown tote bag [King Collection V1]'][0],products['The Crown tote bag [King Collection V1]'][1])
                    elif p == "Anno Domini tote bag [King Collection V1]":
                        cashback = cashback + cashbackCalc(0.15, products['Anno Domini tote bag [King Collection V1]'][0], products['Anno Domini tote bag [King Collection V1]'][1])
                    elif p == "INRI tote bag":
                        cashback = cashback + cashbackCalc(0.15, products['INRI tote bag'][0], products['INRI tote bag'][1])

                instance.referer_cashback = splitCashback(instance.referer_cashback, cashback)
                instance.referee_cashback = splitCashback(instance.referee_cashback, cashback)
                instance.save()  

            if instance.merchant.name == "Singaplex":
                instance.referer_cashback = round(decimal.Decimal(instance.totalAmt) * decimal.Decimal(0.075), 2)
                instance.referee_cashback = round(decimal.Decimal(instance.totalAmt) * decimal.Decimal(0.075), 2)
                instance.save()

            if instance.merchant.name == "Do-Not-Cross":
                products = instance.products
                products = json.loads(str(products))
                
                cashback = 0
                for p in products:
                    if p == "BURNED BEIGE":
                        cashback = cashback + cashbackCalc(0.15, products['BURNED BEIGE'][0], products['BURNED BEIGE'][1])
                    elif p == "DO NOT CROSS X ABEL TAN":       
                        cashback = cashback + cashbackCalc(0.0425, products['DO NOT CROSS X ABEL TAN'][0], products['DO NOT CROSS X ABEL TAN'][1])
                
                instance.referer_cashback = splitCashback(instance.referer_cashback, cashback)
                instance.referee_cashback = splitCashback(instance.referee_cashback, cashback)
                instance.save()       
                
            if instance.merchant.name == "Jemaime":
                instance.referer_cashback = round(decimal.Decimal(instance.totalAmt) * decimal.Decimal(0.05), 2)
                instance.referee_cashback = round(decimal.Decimal(instance.totalAmt) * decimal.Decimal(0.05), 2)
                instance.save()

            #update referrer wallet
            referer = instance.referer_username
            updateWallet(referer, instance.referer_cashback, True)

    if instance.webhook != None and instance.orderRef_obj != None:
        if User.objects.filter(email=instance.referee_email).exists():
            referee = User.objects.filter(email=instance.referee_email)[0]
            updateWallet(referee, instance.referee_cashback, False)

            instance.referee_username = referee.username
            instance.referee_has_account = True
            instance.save()
            
            #send email to referrer with an account
            sendEmailHelper('Successful Referral', 'referrals/success-referral.html', {
                'referer': referer, 
                'wallet': instance.referer_cashback, 
                'referee': User.objects.get(username = instance.referee_username)
            }, referer.email)


            #send email to referee with an account
            sendEmailHelper('Successful Purchase', 'referrals/success-referee.html', {
                'referee': referee,
                'referer': instance.referer_username.username, 
                'cashback': instance.referee_cashback
            }, instance.referee_email)

        else:
            newOrphan = OrphanList.objects.create(
                refereeEmail = instance.referee_email,
                referee_cashback = instance.referee_cashback,
                referral_obj = instance
            )
            newOrphan.save()

            #send email to referrer without an account
            sendEmailHelper('Successful Referral!', 'referrals/success-referral.html', {
                'referer': referer, 
                'wallet': instance.referer_cashback, 
                'referee': instance.referee_email
            }, referer.email)

            #send email to referrer with an account
            sendEmailHelper('Successful Purchase!', 'referrals/success-referee-no-acc.html', {
                'referer': instance.referer_username.username, 
                'cashback': instance.referee_cashback
            }, instance.referee_email)