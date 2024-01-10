from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name','revenue','strength')


@admin.register(Analyst)
class AnalystAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)



@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name','project_type','project_code','LOI')


@admin.register(Incentive)
class IncentiveAdmin(admin.ModelAdmin):
    list_display = ('project','Unique_identifier')


@admin.register(ProjectInterview)
class ProjectInterviewAdmin(admin.ModelAdmin):
    list_display = ('project','interview_duration','interview_date')


@admin.register(Respondent)
# class HodAdmin(admin.ModelAdmin):
#     list_display = ('name','job','email','')


@admin.register(RoleMaster)
class RoleMasterAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Hod)
class HodAdmin(admin.ModelAdmin):
    list_display = ('name','email')



@admin.register(TeamLead)
class TeamLeadAdmin(admin.ModelAdmin):
    list_display = ('name','email')


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('name','email')


@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ('email','username','password','role','user_manager','hod_name','is_active')


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email','username','role','user_manager','hod_name','department','mobile','is_active','is_staff')

# admin.site.register(CustomUser, UserAdmin)
