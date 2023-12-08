# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Job Master
class Job(models.Model):
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


# Country Master
class Country(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

# Industry Master
class Industry(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Company Table
class Company(models.Model):
    name = models.CharField(max_length=255)
    revenue = models.CharField(max_length=255)
    strength = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Analyst Master
class Analyst(models.Model):
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# Department Master
class Department(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Project Table
class Project(models.Model):
    name = models.CharField(max_length=255)
    project_type = models.CharField(max_length=255)
    project_code = models.CharField(max_length=255)
    LOI = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Incentive Table
class Incentive(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    Unique_identifier = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Unique_identifier


# Project Interview
class ProjectInterview(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    interview_duration = models.CharField(max_length=255)
    interview_date = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


# Respondent Table
class Respondent(models.Model):
    name = models.CharField(max_length=255)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    email = models.EmailField()
    user_manager = models.CharField(max_length=255)
    user_manager_email = models.EmailField()
    hod_email = models.EmailField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    profile_link = models.CharField(max_length=255)
    meeting_link = models.CharField(max_length=255)
    analyst = models.ForeignKey(Analyst, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    incentive = models.ForeignKey(Incentive, on_delete=models.CASCADE)
    project_interview = models.ForeignKey(ProjectInterview, on_delete=models.CASCADE)
    team_lead = models.CharField(max_length=255,blank=True,null=True)
    Department = models.CharField(max_length=255,blank=True,null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


# Role Master
class RoleMaster(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# HOD Name
class Hod(models.Model):
    name = models.CharField(max_length=255,blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
# Team Lead Name
class TeamLead(models.Model):
    name = models.CharField(max_length=255,blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Assistance Manager / Manager 
class Manager(models.Model):
    name = models.CharField(max_length=255,blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
# Register
class Register(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=255, null=True, blank=True)
    user_manager = models.CharField(max_length=255, null=True, blank=True)
    hod_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


# Create your models here.

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, username, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email,username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, username=username,password=password, **extra_fields)



class CustomUser(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(max_length=255, null=True, blank=True)
    user_manager = models.CharField(max_length=255, null=True, blank=True)
    hod_name = models.CharField(max_length=255, null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    mobile = models.CharField(max_length=255, null=True, blank=True)
    token = models.CharField(max_length=255, null=True, blank=True)
    otp = models.CharField(max_length=255, null=True, blank=True)
    is_superviser = models.CharField(max_length=255, null=True, blank=True)
    is_category = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.password.startswith("pbkdf2_sha256$"):
            # If the password is not already hashed, securely hash it
            self.set_password(self.password)
        super().save(*args, **kwargs)


    class Meta:
        permissions = [
            ("view_customuser_object", "Can view"),
            ("edit_customuser_object", "Can edit"),
            ("delete_customuser_object", "Can delete"),
            ("create_customuser_object", "Can create"),
        ]

    




# class CustomUser(AbstractUser):
#     email = models.EmailField(_("email address"), unique=True)
#     username = models.CharField(max_length=100)
#     role = models.CharField(max_length=255, null=True, blank=True)
#     user_manager = models.CharField(max_length=255, null=True, blank=True)
#     hod_name = models.CharField(max_length=255, null=True, blank=True)
#     department = models.CharField(max_length=255, null=True, blank=True)
#     mobile = models.CharField(max_length=255, null=True, blank=True)
#     token = models.CharField(max_length=255, null=True, blank=True)
#     otp = models.CharField(max_length=255, null=True, blank=True)
#     is_superviser = models.CharField(max_length=255, null=True, blank=True)
#     is_category = models.CharField(max_length=255, null=True, blank=True)
#     is_active = models.BooleanField(default=False)
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
    
#     REQUIRED_FIELDS = ['username']