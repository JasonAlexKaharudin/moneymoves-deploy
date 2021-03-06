from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from referrals.models import OrphanList, orphanReceipt, receipts
from django.db.models.signals import post_save
from django.dispatch import receiver

User._meta.get_field('email')._unique = True

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    Phone_Number = PhoneNumberField(blank=False, unique=True)
    wallet= models.DecimalField(max_digits=6, decimal_places=2, default=0)
    num_of_refers = models.IntegerField(default=0)
    links_created = models.IntegerField(default=0)
    signup_refs = models.IntegerField(default=0)
    code = models.CharField(max_length=30, blank= True)
    recommended_by = models.ForeignKey(User, on_delete=CASCADE, blank=True, related_name="ref_by", null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

@receiver(post_save, sender = Profile)
def post_save_profile(sender, instance, created, *args, **kwargs):
    if created:
        #check orphans for partner orders
        if OrphanList.objects.filter(refereeEmail = instance.user.email).exists():
            # update the username in the ref object
            ref_obj = OrphanList.objects.get(refereeEmail = instance.user.email).referral_obj
            ref_obj.referee_username = instance.user.username
            ref_obj.referee_has_account = True
            
            #update the wallet and num refers of referee
            referee = User.objects.get(username = ref_obj.referee_username)
            referee.profile.wallet = referee.profile.wallet + ref_obj.referee_cashback
            referee.profile.num_of_refers = referee.profile.num_of_refers + 1
            referee.profile.save()

            ref_obj.save()
         
            #delete the orphan list object
            obj = OrphanList.objects.get(refereeEmail = instance.user.email)
            obj.delete()
        
        #check orphan receipts for amazon order
        if orphanReceipt.objects.filter(referee = instance.Phone_Number).exists():
            #update username of referee on receipt object
            receipt_obj = orphanReceipt.objects.get(referee = str(instance.Phone_Number)).referral_obj
            receipt_obj.referee = instance.user.username
            print(receipt_obj.referee )
            receipt_obj.save()

            #update the number of refers of referee
            referee = User.objects.get(username = receipt_obj.referer)
            referee.profile.num_of_refers = referee.profile.num_of_refers + 1
            referee.profile.save()

            obj = orphanReceipt.objects.get(referee = str(instance.Phone_Number))
            obj.delete()
