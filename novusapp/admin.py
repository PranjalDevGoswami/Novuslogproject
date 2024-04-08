from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin

@admin.register(Country)
class CountryAdmin(ImportExportModelAdmin):
    list_display = ("name",)

@admin.register(Industry)
class IndustryAdmin(ImportExportModelAdmin):
    list_display = ('name','is_active', 'created_at', 'updated_at')
    
@admin.register(Industry_Sub_Cate)
class IndustryAdmin(ImportExportModelAdmin):
    list_display = ('name','is_active', 'created_at', 'updated_at')    

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name','revenue','revenue_currency_type')
    
@admin.register(Currency_Type)
class CompanyAdmin(ImportExportModelAdmin):
    list_display = ('currency_type',)
    
@admin.register(Analyst)
class AnalystAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')

@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ('name',)

@admin.register(ProjectType)
class ProjectTypeAdmin(ImportExportModelAdmin):
    list_display = ('name',)
    
@admin.register(Project)
class ProjectAdmin(ImportExportModelAdmin):
    list_display = ('name','project_type','project_code','LOI')
      
@admin.register(IncentiveType)
class IncentiveTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
@admin.register(PhoneNumber)
class PhoneNumberAdmin(ImportExportModelAdmin):
    list_display = ('phone_number',)
    
@admin.register(PhoneCode)
class PhoneCodeAdmin(ImportExportModelAdmin):
    list_display = ('phone_code',)
    
@admin.register(Incentive)
class IncentiveAdmin(admin.ModelAdmin):
    list_display = ('project','Unique_identifier')

@admin.register(ProjectInterview)
class ProjectInterviewAdmin(ImportExportModelAdmin):
    list_display = ('project','interview_date')

@admin.register(Respondent)
# class HodAdmin(admin.ModelAdmin):
#     list_display = ('name','job','email','')

@admin.register(RoleMaster)
class RoleMasterAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Hod)
class HodAdmin(admin.ModelAdmin):
    list_display = ('name','email','dep','Designation',)

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
    list_display = ('email','username','role','user_manager','hod_name','mobile','is_active','is_staff')

# admin.site.register(CustomUser, UserAdmin)
