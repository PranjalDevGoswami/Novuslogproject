from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import *
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from django.contrib.auth import get_user_model
from django.contrib import messages
UserModel = get_user_model()


@receiver(post_save, sender=Respondent)
def update_payment_status(sender, instance, created, **kwargs):
    if instance.pay_status == 1:
        # Payment was completed for this respondent, update payment status in payment_status table
        payment = payment_status.objects.create(
            respondents=instance,
            respondent_id=instance.id,
            respondent_email=instance.email,
            country=instance.country.name,
            payment_id=instance.payment_id,
            incentive_type=instance.incentive_type,
            payment_amount=int(instance.incentive.Unique_identifier),
            payment_status=instance.pay_status,
            remark='Payment completed',
        )
        payment.save()  # Save the payment data
        
   

from django.db import transaction
@receiver(post_save, sender=CustomUser)
def update_hod_master(sender, instance, created, **kwargs):
    if created and instance.hod_name:
        with transaction.atomic():
            hod_obj = Hod.objects.create(
                name=instance.hod_name,
                email=instance.email,
                dep=instance.dep
            )
    elif instance.hod_name:
        with transaction.atomic():
            try:
                hod_obj = Hod.objects.get(email=instance.email)
                hod_obj.name = instance.hod_name
                hod_obj.dep = instance.dep
                hod_obj.save()
            except Hod.DoesNotExist:
                hod_obj = Hod.objects.create(
                    name=instance.hod_name,
                    email=instance.email,
                    dep=instance.dep
                )
    else:
        pass