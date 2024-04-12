from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import *
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
            update_respondent_id(instance, 'job')
            update_respondent_id(instance, 'industry')
            update_respondent_id(instance, 'company')
            update_respondent_id(instance, 'analyst')
            update_respondent_id(instance, 'project')
            update_respondent_id(instance, 'incentive')
            update_respondent_id(instance, 'project_interview')
            update_respondent_id(instance, 'PhoneNumber')
