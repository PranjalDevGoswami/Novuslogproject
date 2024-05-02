from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import *
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from django.contrib.auth import get_user_model
from django.contrib import messages
UserModel = get_user_model()

# Reusable function to update respondent_id for related model
def update_respondent_id(instance, related_model):
    related_instance = getattr(instance, related_model)
    related_instance.respondent_id = instance.pk
    related_instance.save()

# Define signal receiver to update master records after saving Respondent
@receiver(post_save, sender=Respondent)
def update_master_records(sender, instance, created, **kwargs):
    if created: 
        with transaction.atomic():  
            update_respondent_id(instance, 'country')
            update_respondent_id(instance, 'respondent_phone')
            update_respondent_id(instance, 'industry')
            update_respondent_id(instance, 'company')
            update_respondent_id(instance, 'analyst')
            update_respondent_id(instance, 'project')
            update_respondent_id(instance, 'project_interview')
            update_respondent_id(instance, 'incentive')
            



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
        
        
# @receiver(post_save, sender=CustomUser)
# def update_hod_master(sender, instance, created, **kwargs):
#     try:
#         if created and instance.hod_name:
#             hod_obj = Hod.objects.create(
#                 name=instance.hod_name,
#                 email=instance.email,
#                 dep=instance.dep
#             )
#             hod_obj.save()
            
#         else:
#             try:
#                 user_instance = UserModel.objects.get(id=instance.id)
#                 hod_obj = Hod.objects.get(email=user_instance.email)
#                 hod_obj.name = instance.hod_name
#                 hod_obj.email = instance.email
#                 hod_obj.dep = instance.dep
#                 hod_obj.save()
#             except Hod.DoesNotExist:
#                 pass         
#     except Exception as e:
#         pass
        

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