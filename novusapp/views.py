# Create your views here.
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.utils import timezone
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.core.serializers import serialize
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import yaml
from django.core import signing
from django.contrib.auth.decorators import login_required
from .decorators import unauthenitcated_user,role_required
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .send_voucher_email import send_voucher_order

import io
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib import messages
from django.conf import settings
from decimal import Decimal
# from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
import paypalrestsdk
from .forms import *
from paypal.standard.forms import PayPalPaymentsForm
from django.http import HttpResponseBadRequest
from django.core.files.storage import FileSystemStorage
import pandas as pd 
from django.db import transaction
import uuid
from urllib.parse import urlencode
import json


UserModel = get_user_model() 

credentials = yaml.load(open('./novusproject/credentials.yml','r'),Loader=yaml.FullLoader)
host_url = credentials['hosted_url']


''' Define a list of valid email domain '''

VALID_EMAIL_DOMAINS = ['unimrkt.com', 'novusinsights.com','unimrkthealth.com']

def is_valid_email_domain(email):
    ''' Split the email address to get the domain part '''
    domain = email.split('@')[-1]

    ''' Check if the email is blank '''
    if not email:
        return False

    ''' Check if the domain is in the list of valid domains '''
    if domain in VALID_EMAIL_DOMAINS:
        return True
    return False


def register(request):
    hod = Hod.objects.all().values('name')
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['pass']
        confpassword = request.POST['conf_pass']
        try:
            novus_hod = request.POST['hod']
        except:
            pass

        ''' Check if the email already exists '''
        try:
            existing_user = Register.objects.get(email=email)
            messages.error(request, 'This email is already registered.', extra_tags="alert-danger")
            return redirect('/register')
        except Register.DoesNotExist:
            pass

        ''' Check if the passwords match '''
        if password != confpassword:
            messages.error(request, 'Passwords do not match.',extra_tags="alert-danger")
            return redirect('register')

        ''' Validate email domain '''
        if not is_valid_email_domain(email):
            if not email:
                messages.error(request, 'Please fill in the email field.', extra_tags="alert-danger")
            else:
                messages.error(request, 'Invalid email domain. Please use a valid domain.',extra_tags="alert-danger")
            return redirect('register')
        
        ''' Create a new user '''
        try:
            user = Register.objects.create(email=email,username=username,password=password,hod_name=novus_hod)
            user.save()
            messages.success(request, 'Registration successful. You can wait some time for defining your role.', extra_tags="alert-success")
            return redirect('/')
        except Exception as e:
            print(f"\n\n ERROR :: {e} \n\n")
            messages.error(request, f'An error occurred: {str(e)}',extra_tags="alert-danger")
            return redirect('register')
    
    context = {'novushod':hod}
    return render(request, 'novusapp/register.html',context)


@login_required
@role_required(allowed_roles=['HOD'])
def confirm_registration(request,id):
    role = RoleMaster.objects.all().values('name')
    team_manager = Manager.objects.all().values('name')
    if request.session.has_key('currentuser_id'):
        currentid =  request.session['currentuser_id']
        customuserdata = CustomUser.objects.filter(id=currentid).values('hod_name','email')
        current_hod = (customuserdata[0]['hod_name'])
        hod_email = (customuserdata[0]['email'])
        complex_obj = Register.objects.filter(is_active=0,hod_name=current_hod).values('id', 'email', 'password', 'hod_name')
        total_user = complex_obj.count()
 
        ''' Create a list of dictionaries to store user-specific data '''
        user_data_list = []
 
        for userdata in complex_obj:
            user_data = {
                'id': userdata['id'],
                'email': userdata['email'],
                'password': userdata['password'],
                'hod_name': userdata['hod_name'],
            }
            user_data_list.append(user_data)
   
        if request.method == 'POST':
            role1 = request.POST['user_role1']
            try:
                user_manager = request.POST['user_manager']
            except:
                pass
            if role1 == 'Team Lead':
                id = signing.loads(id)
                user_manager = user_manager
                try:
                    email1 = Register.objects.get(id=id).email
                except Register.DoesNotExist:
                    raise ValueError("Please register manager then assign to teamlead.")
                username = Register.objects.get(id=id).username
                password1 = Register.objects.get(id=id).password
                hodname = Register.objects.get(id=id).hod_name
 
                try:
                    existing_user_active = Register.objects.get(id=id).is_active
                    if existing_user_active == 1:
                        
                        Register.objects.filter(id=id).update(role=role1,user_manager=user_manager)
                        ''' Retrieve the user '''
                        user1 = get_object_or_404(CustomUser, email=email1)
 
                        ''' Retrieve the group '''
                        try:
                            group = Group.objects.get(name=role1)
                        except Group.DoesNotExist:
                            ''' Handle the case where the group doesn't exist '''
                            return HttpResponse(f"Group '{role1}' does not exist.", status=400)
 
                        ''' Add the user to the group '''
                        user1.groups.clear()
                        user1.groups.add(group)
 
                        ''' Save the changes to the user '''
                        user1.save()
                        messages.success(request, 'This id user role and AM/Manager updated Successfully.',extra_tags="alert-success")
                        email1 = Register.objects.get(id=id).email
                        username = Register.objects.get(id=id).username
                        CustomUser.objects.filter(email=email1).update(role=role1, user_manager=user_manager)
                        try:
                            TeamLead.objects.create(name=username,email=email1)
                            Manager.objects.filter(name=username,email=email1).delete()
                        except:
                            pass
                        return redirect('/hod_dashboard')
                    else:
                        TeamLead.objects.create(email=email1,name=username)
                        existing_user = Register.objects.filter(id=id).update(is_active=1,role=role1,user_manager=user_manager)
                        user = CustomUser.objects.create_user(email=email1,username=username, password=password1,hod_name=hodname,role=role1,user_manager=user_manager,is_active=1,is_staff=1)
                        
                        user.save()
                        ''' Retrieve the user '''
                        user1 = get_object_or_404(CustomUser, email=email1)
 
                        ''' Retrieve the group '''
                        try:
                            group = Group.objects.get(name=role1)
                        except Group.DoesNotExist:
                            ''' Handle the case where the group doesn't exist '''
                            return HttpResponse(f"Group '{role1}' does not exist.", status=400)
 
                        ''' Add the user to the group '''
                        user1.groups.add(group)
 
                        ''' Save the changes to the user '''
                        user1.save()
                        messages.success(request, 'Registration Completed',extra_tags="alert-success")
                        return redirect('/hod_dashboard')
                except Register.DoesNotExist:
                    pass
 
            if role1 == 'AM/Manager':
                id = signing.loads(id)
                email1 = Register.objects.get(id=id).email
                username = Register.objects.get(id=id).username
                password1 = Register.objects.get(id=id).password
                hodname = Register.objects.get(id=id).hod_name
                user_manager = hodname
 
                try:
                    existing_user_active = Register.objects.get(id=id).is_active
                    if existing_user_active == 1:
 
                        Register.objects.filter(id=id).update(role=role1,user_manager=user_manager)
                        user1 = get_object_or_404(CustomUser, email=email1)
 
                        ''' Retrieve the group '''
                        try:
                            group = Group.objects.get(name=role1)
                        except Group.DoesNotExist:
                            ''' Handle the case where the group doesn't exist '''
                            return HttpResponse(f"Group '{role1}' does not exist.", status=400)
 
                        ''' Add the user to the group '''
                        user1.groups.clear()
                        user1.groups.add(group)
 
                        ''' Save the changes to the user '''
                        user1.save()
                        messages.success(request, 'This id user role and AM/Manager updated Successfully.',extra_tags="alert-success")
                        CustomUser.objects.filter(email=email1).update(role=role1,user_manager=user_manager)
                        
                        print('$$$$$$$$$$$$$$$$$$')
                        try:
                            Manager.objects.create(name=username,email=email1)
                            TeamLead.objects.filter(name=username,email=email1).delete()
                        except:
                            pass
                        return redirect('/hod_dashboard')
                    else:
                        print('***************12345566')
                        Manager.objects.create(email=email1,name=username)
                        existing_user = Register.objects.filter(id=id).update(is_active=1,role=role1,user_manager=user_manager)
                        user = CustomUser.objects.create_user(email=email1,username=username, password=password1,hod_name=hodname,role=role1,user_manager=user_manager,is_active=1,is_staff=1)
                        user.save()
                        
                        ''' Retrieve the user '''
                        user1 = get_object_or_404(CustomUser, email=email1)
 
                        ''' Retrieve the group '''
                        try:
                            group = Group.objects.get(name=role1)
                        except Group.DoesNotExist:
                            ''' Handle the case where the group doesn't exist '''
                            return HttpResponse(f"Group '{role1}' does not exist.", status=400)
 
                        ''' Add the user to the group '''
                        user.groups.clear()
                        user1.groups.add(group)
 
                        ''' Save the changes to the user '''
                        user1.save()
                        messages.success(request, 'Registration Completed',extra_tags="alert-success")
                        return redirect('/hod_dashboard')
                except Register.DoesNotExist:
                    pass
                
            if role1 == 'HOD':
                id = signing.loads(id)
                email1 = Register.objects.get(id=id).email
                username = Register.objects.get(id=id).username
                password1 = Register.objects.get(id=id).password
                hodname = Register.objects.get(id=id).hod_name
                user_manager = ''
 
                try:
                    existing_user_active = Register.objects.get(id=id).is_active
                    if existing_user_active == 1:
                        
                        Register.objects.filter(id=id).update(role=role1,user_manager=user_manager)
                        ''' Retrieve the user '''
                        user1 = get_object_or_404(CustomUser, email=email1)
 
                        ''' Retrieve the group '''
                        try:
                            group = Group.objects.get(name=role1)
                        except Group.DoesNotExist:
                            ''' Handle the case where the group doesn't exist '''
                            return HttpResponse(f"Group '{role1}' does not exist.", status=400)
 
                        ''' Add the user to the group '''
                        user1.groups.clear()
                        user1.groups.add(group)
 
                        ''' Save the changes to the user '''
                        user1.save()
                        messages.success(request, 'This id user role and AM/Manager updated Successfully.',extra_tags="alert-success")
                        email1 = Register.objects.get(id=id).email
                        username = Register.objects.get(id=id).username
                        CustomUser.objects.filter(email=email1).update(role=role1)
                        try:
                            Hod.objects.create(name=username,email=email1)
                        except:
                            pass
                        return redirect('/hod_dashboard')
                    else:
                        existing_user = Register.objects.filter(id=id).update(is_active=1,role=role1,user_manager=user_manager)
                        user = CustomUser.objects.create_user(email=email1,username=username, password=password1,hod_name=hodname,role=role1,user_manager=user_manager,is_active=1,is_staff=1)
                        
                        user.save()
                        ''' Retrieve the user '''
                        user1 = get_object_or_404(CustomUser, email=email1)
 
                        ''' Retrieve the group '''
                        try:
                            group = Group.objects.get(name=role1)
                        except Group.DoesNotExist:
                            ''' Handle the case where the group doesn't exist '''
                            return HttpResponse(f"Group '{role1}' does not exist.", status=400)
 
                        ''' Add the user to the group '''
                        user1.groups.add(group)
 
                        ''' Save the changes to the user '''
                        user1.save()
                        messages.success(request, 'Registration Completed',extra_tags="alert-success")
                        return redirect('/hod_dashboard')
                except Register.DoesNotExist:
                    pass
                
         
            email1 = Register.objects.get(id=id).email
            username = Register.objects.get(id=id).username
            password1 = Register.objects.get(id=id).password
            hodname = Register.objects.get(id=id).hod_name
            
            ''' Check if the email already exists '''
            try:
                existing_user_active = Register.objects.get(id=id).is_active
                if existing_user_active == 1:
                    Register.objects.filter(id=id).update(role=role1,user_manager=user_manager)
                    ''' Retrieve the user '''
                    user1 = get_object_or_404(CustomUser, email=email1)
 
                    ''' Retrieve the group '''
                    try:
                        group = Group.objects.get(name=role1)
                    except Group.DoesNotExist:
                        ''' Handle the case where the group doesn't exist '''
                        return HttpResponse(f"Group '{role1}' does not exist.", status=400)
 
                    ''' Add the user to the group '''
                    user1.groups.clear()
                    user1.groups.add(group)
 
                    ''' Save the changes to the user '''
                    user1.save()
                    messages.success(request, 'This id user role and AM/Manager updated Successfully.',extra_tags="alert-success")
                    CustomUser.objects.filter(email=email1).update(role=role1)
                    try:
                        TeamLead.objects.create(name=username,email=email1)
                    except:
                        pass
                    return redirect('/hod_dashboard')
            except Register.DoesNotExist:
                pass
 
            ''' Create a new user '''
            try:
                
                existing_user = Register.objects.filter(id=id).update(is_active=1,role=role1,user_manager=user_manager)
                user = CustomUser.objects.create_user(email=email1,username=username,password=password1,hod_name=hodname,role=role1,user_manager=user_manager,is_active=1,is_staff=1)
                user.save()
                ''' Retrieve the user '''
                user1 = get_object_or_404(CustomUser, email=email1)
 
                ''' Retrieve the group '''
                try:
                    group = Group.objects.get(name=role1)
                except Group.DoesNotExist:
                    ''' Handle the case where the group doesn't exist '''
                    return HttpResponse(f"Group '{role1}' does not exist.", status=400)
 
                ''' Add the user to the group '''
                user1.groups.add(group)
 
                ''' Save the changes to the user '''
                user1.save()
                messages.success(request, 'Registration Completed',extra_tags="alert-success")
                return redirect('/hod_dashboard')
              
            except Exception as e:
                print(f"\n\n ERROR :: {e} \n\n")
                messages.error(request, f'An error occurred: {str(e)}')
                return redirect('register')
            
        
        context = {
            'total': total_user,
            'user_data_list': user_data_list,
            'hod':current_hod,
            'role':role,
            'team':team_manager,
            'id':id,
            'host_url': host_url
           
        }
 
        return render(request, 'novusapp/confirm_registration.html',context)
    
    return render(request, 'novusapp/confirm_registration.html')

def login_view(request):
    ''' If user is already authenticated, redirect them to their dashboard '''
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')

    ''' Continue with the regular login logic if not authenticated '''
    if request.method == 'POST':
        email = request.POST.get('email')
        user_password = request.POST.get('login_password')

        ''' Authenticate the user '''
        user = authenticate(request, email=email, password=user_password)

        if user is not None and user.is_active:
            request.session['currentuser_id'] = user.id
            login(request, user)

            ''' Redirect to the dashboard if already authenticated '''
            next_url = request.GET.get('next', None)
            if next_url and not next_url.startswith('/login'):
                return redirect(next_url)

            return redirect('dashboard_redirect') 

        else:
            messages.error(request, 'Invalid login credentials.', extra_tags="alert-danger")

    return render(request, 'novusapp/login.html')


def download_excel(respondents):
    # Create an in-memory output stream for storing the Excel file
    output = io.BytesIO()
    
    # Create a new workbook and select the active worksheet
    wb = Workbook()
    ws = wb.active
 
    # Set the height of the header row
    ws.row_dimensions[1].height = 22  # Set height in points (1 point = 1/72 inch)
    
    # Write headers with colors and enable filter
    headers = [
        'Respondent Name', 'Email', 'Phone Number', 'Job Title', 'Company', 'Country',
        'Industry', 'Interviewer Name', 'Project', 'Project Type', 'Company Revenue',
        'Incentive', 'Interview Duration', 'Interview Date', 'Team Lead',
        'Manager', 'Department', 'Status'
    ]
    
    for idx, header in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=idx, value=header)
        # Apply color to the header cell
        cell.fill = PatternFill(start_color="FFCCCB", end_color="FFCCCB", fill_type="solid")
 
    # Enable filtering for the headers
    ws.auto_filter.ref = ws.dimensions
    
    # Write data rows
    for respondent in respondents:
        # Construct the row with proper handling of potential None values
        row = [
            f"{respondent.name} {(respondent.middle_name or '')} {(respondent.last_name or '')}".strip(),
            respondent.respondent_email,
            f"{(respondent.phone_code or '')} {(respondent.respondent_phone or '')}".strip() if respondent.respondent_phone else '',
            respondent.job if respondent.job else '',  # Assuming `job` is an object with a `title` attribute
            respondent.company_name if respondent.company_name else '',
            respondent.country.name if respondent.country else '',
            respondent.industry.name if respondent.industry else '',
            respondent.analyst if respondent.analyst else '',
            respondent.project_name if respondent.project_name else '',
            respondent.project_type.name if respondent.project_type else '',  # Ensure `project_type` is not None
            f"{respondent.company_revenue or ''} {respondent.currency_type.currency_type or ''}".strip() if respondent.company_revenue else '',
            f"{respondent.incentive_amount or ''} {respondent.incentive_currency_type or ''}".strip() if respondent.incentive_amount else '',
            f"{str(respondent.interview_duration_hours) or ''}hr: {str(respondent.interview_duration_minutes) or ''}min".strip() if respondent.interview_duration_hours else '',
            respondent.interview_date if respondent.interview_date else '',
            respondent.team_lead or '',
            respondent.user_manager or '',
            respondent.Department or '',
            'Pending' if respondent.is_active == 0 else 'Complete'
        ]
        # Ensure all elements are strings before appending
        row = [str(cell) for cell in row]
        ws.append(row)
    
    # Save the workbook to the output stream
    wb.save(output)
    output.seek(0)
    
    # Set response headers to serve the Excel file
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=respondents_data.xlsx"
    
    return response
 


@login_required
def dashboard_redirect(request):
    ''' If user is already authenticated, redirect to their dashboard '''
    if request.user.is_authenticated:
        if request.user.groups.filter(name="Team Lead").exists():
            return redirect('user_dashboard')

        elif request.user.groups.filter(name="AM/Manager").exists():
            return redirect('manager')

        elif request.user.groups.filter(name="HOD").exists():
            try:
                hod_name = Hod.objects.get(email=request.user.email).name
            except Hod.DoesNotExist:
                hod_name = ""
            CustomUser.objects.filter(id=request.user.id).update(hod_name=hod_name)
            messages.success(request, "Successfully logged in.", extra_tags="alert-success")
            return redirect('hod_dashboard')

        elif request.user.is_superuser:
            return redirect('admin:index')

    ''' If not authenticated, handle as before '''
    return redirect('/')


@login_required
@role_required(allowed_roles=['Team Lead'])
def user_dashboard(request):
    if request.session.has_key('currentuser_id'):
        userid = request.session['currentuser_id']
        custom_user_obj = CustomUser.objects.get(id=userid)
        TeamLeadname = custom_user_obj.username
        TeamLead_email = custom_user_obj.email
        user_manager = custom_user_obj.user_manager
        
        try:
            department = custom_user_obj.dep.name
        except AttributeError:
            department = ""

        try:
            hod_name = custom_user_obj.hod_name
            hod_email = Hod.objects.filter(name=hod_name)[0].email
        except (AttributeError, IndexError):
            messages.error(request, "Your Registration is not confirmed. Please wait some time and then login.", extra_tags="alert-danger")
            return redirect('/')

        try:
            user_manager_email = Manager.objects.get(name=user_manager).email
        except Manager.DoesNotExist:
            user_manager_email = TeamLead_email

        industries = Industry.objects.all()
        industry_data = {industry: industry.subindustry.all() for industry in industries if industry.subindustry.exists()}
        mycountry = Country.objects.values('id', 'name').distinct()
        currency_type = Currency_Type.objects.all().values('id', 'currency_type')
        Project_Type = ProjectType.objects.all().values('id', 'name')
        Incentive_Type = IncentiveType.objects.all().values('id', 'name')
        phone_code = PhoneCode.objects.all().values('id', 'phone_code')
        incentive_currency_type = Incentive_Currency_Type.objects.all().values('id', 'currency_type')

        if request.method == 'POST':
            try:
                # Get the data from the POST request
                respondent_name = request.POST.get('respondent_name')
                middle_name = request.POST.get('middle_name')
                last_name = request.POST.get('last_name')
                email = request.POST.get('email')
                job_title = request.POST.get('job_title')
                country_id = request.POST.get('country')
                phone_number = request.POST.get('phone_number')
                phone_code_id = request.POST.get('Phone_number_code')
                industry_id = request.POST.get('industry')
                company_name = request.POST.get('company')
                company_revenue_value = request.POST.get('company_revenue')
                client_name = request.POST.get('client_name')
                company_revenue_currency_type_value = request.POST.get('company_revenue_currency_type')
                analyst_name = request.POST.get('analyst')
                project_type_id = request.POST.get('project_type')
                project_name = request.POST.get('project')
                project_code = request.POST.get('project_code')
                interview_duration_hours = request.POST.get('interview_duration_hours')
                interview_duration_minutes = request.POST.get('interview_duration_minutes')
                interview_date = request.POST.get('interview_date')
                incentive_type_id = request.POST.get('incentive_type')
                incentive_amount = request.POST.get('incentive')
                incentive_code = request.POST.get('incentive_code')
                incentive_currency_type_id = request.POST.get('incentive_currency_type')
                linkdin_profile = request.POST.get('linkdin_profile')
                payment_mode = request.POST.get('payment_mode')
                pay_status = request.POST.get('pay_status') == 'on'
                # Fetch the related objects
                country = get_object_or_404(Country, id=country_id)
                industry = get_object_or_404(Industry_Sub_Cate, id=industry_id)
                project_type = get_object_or_404(ProjectType, id=project_type_id)
                phone_code = get_object_or_404(PhoneCode, id=phone_code_id)
                incentive_type = get_object_or_404(IncentiveType, id=incentive_type_id)
                incentive_currency_type = get_object_or_404(Incentive_Currency_Type, id=incentive_currency_type_id)
                company_currency_type_value = get_object_or_404(Currency_Type, id=company_revenue_currency_type_value)
                selected_voucher = request.POST.get('selected_voucher','') 
                voucher_value = request.POST.get('voucher_value','')
                voucher_quantity = request.POST.get('number','')
                # Create the Respondent instance and associate it with the related records
                respondent = Respondent.objects.create(
                    name=respondent_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    respondent_email=email,
                    custom_user=custom_user_obj,
                    respondent_phone=phone_number,
                    phone_code=phone_code,
                    job=job_title,
                    email=TeamLead_email,
                    user_manager=user_manager,
                    hod_email=hod_email,
                    user_manager_email=user_manager_email,
                    country=country,
                    industry_sub_cate=industry,
                    company_name=company_name,
                    company_revenue=company_revenue_value,
                    client_name = client_name,
                    currency_type=company_currency_type_value,
                    analyst=analyst_name,
                    project_name=project_name,
                    project_type=project_type,
                    project_code=project_code,
                    interview_duration_hours=interview_duration_hours,
                    interview_duration_minutes=interview_duration_minutes,
                    interview_date=interview_date,
                    incentive_type_id=incentive_type,
                    incentive_code=incentive_code,
                    incentive_currency_type=incentive_currency_type,
                    incentive_amount=incentive_amount,
                    linkdin_profile=linkdin_profile,
                    team_lead=TeamLeadname,
                    Department=department,
                    payment_mode=payment_mode,
                    pay_status=pay_status,
                    voucher_productid = selected_voucher,
                    voucher_value = voucher_value,
                    voucher_quantity = voucher_quantity,
                    is_active=False
                )

                # Save the Respondent instance to the database
                respondent.save()
                if selected_voucher and voucher_value and voucher_quantity:
                    notify_receiver_email = 0
                    notify_admin_email = 0
                    send_voucher_order(selected_voucher, voucher_value, voucher_quantity, notify_receiver_email, notify_admin_email)
                    
    
                messages.success(request, 'Form Submitted Successfully', extra_tags="alert-success")
                return redirect('/user_dashboard')

            except Exception as e:
                messages.error(request, f'Error: {e}', extra_tags="alert-danger")
                return redirect('/user_dashboard')

        context = {
            'industry_data': industry_data,
            'allcountry': mycountry,
            'currency_type': currency_type,
            'Project_Type': Project_Type,
            'Incentive_Type': Incentive_Type,
            'phone_code': phone_code,
            'incentive_currency_type': incentive_currency_type,
            
        }

        return render(request, "novusapp/user_dashboard.html", context)

    return HttpResponse('Please login')




@login_required
@role_required(allowed_roles=['Team Lead'])
def userdata(request):
    if request.session.has_key('currentuser_id'):
        userid = request.session['currentuser_id']
        name = CustomUser.objects.get(id=userid).username
    
        data_type = request.GET.get('type')
        download = request.GET.get('info')
        # items_per_page = int(request.GET.get('items_per_page', 10))
        
        # Default queryset
        respondents = Respondent.objects.filter(custom_user=userid, is_active__in=[0,1]).all()
        print(respondents)

        if download == 'download':
            if data_type == 'self':
                return download_excel(respondents)
            elif data_type == 'all':
                respondents = Respondent.objects.filter(Q(custom_user=userid, is_active=1) | Q(is_active=1)).all()
                return download_excel(respondents)
        else:
            if data_type == 'all':
                respondents = Respondent.objects.filter(Q(custom_user=userid, is_active=1) | Q(is_active=1)).all()
            elif data_type == 'self':
                pass  # Respondents already filtered by default queryset


            context = {
                'respondents': respondents,
                'name': name,

            }
            return render(request, "novusapp/userdata.html", context)

    return HttpResponse('Please Login')



@login_required
@role_required(allowed_roles=['Team Lead'])
def edit_respondent(request, id):
    try:
        respondent_obj = Respondent.objects.get(id=id)
    except Respondent.DoesNotExist:
        messages.error(request, 'Respondent not found', extra_tags="alert-danger")
        return redirect('/user_dashboard')

   
    phone_code = PhoneCode.objects.all().values('id', 'phone_code')
    currency_type = Currency_Type.objects.all().values('id','currency_type')
    incentive_currency_type = Incentive_Currency_Type.objects.all().values('id','currency_type')
    mycountry = Country.objects.all().values('id','name').distinct()
    industries = Industry.objects.all()
    industry_data = {industry: industry.subindustry.all() for industry in industries if industry.subindustry.exists()}
    Incentive_Type = IncentiveType.objects.all().values('id', 'name')
    Project_Type = ProjectType.objects.all().values('id', 'name')
    context = {
        "respondents": [respondent_obj],
        'phone_code': phone_code,
        'currency_type': currency_type,
        'incentive_currency_type' : incentive_currency_type,
        'allcountry': mycountry,
        'industry_data': industry_data,
        'Incentive_Type': Incentive_Type,
        'Project_Type': Project_Type,
    }

    if request.method == "POST":
        respondent_obj = Respondent.objects.get(id=id)
        try:
            # Fetch user object
            userid = request.session.get('currentuser_id')
            custom_user_obj = CustomUser.objects.get(id=userid)

            # Fetch data from POST request
            respondent_name = request.POST.get('respondent_name')
            middle_name = request.POST.get('middle_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            Phone_number_code = request.POST.get('Phone_number_code')
            job_title = request.POST.get('job_title')
            company_name = request.POST.get('company')
            company_revenue_value = request.POST.get('company_revenue')
            company_revenue_currency_type_value = request.POST.get('company_revenue_currency_type')
            country_name = request.POST.get('country')
            industry_name = request.POST.get('industry')
            incentive_code = request.POST.get('incentive_code')
            analyst_name = request.POST.get('analyst')
            incentive_type_id = request.POST.get('incentive_type')
            client_name = request.POST.get('client_name')
            project_name = request.POST.get('project')
            project_code = request.POST.get('project_code')
            project_type_id = request.POST.get('project_type')
            incentive_amount = request.POST.get('incentive')
            incentive_code_name = request.POST.get('incentive_code')
            incentive_currency_type_id = request.POST.get('incentive_currency_type')
            interview_date = request.POST.get('interview_date')
            interview_duration_hours = request.POST.get('interview_duration_hours')
            interview_duration_minutes = request.POST.get('interview_duration_minutes')
            linkdin_profile = request.POST.get('linkdin_profile')
           
            country = get_object_or_404(Country, id=country_name)
            industry = get_object_or_404(Industry_Sub_Cate, id=industry_name)
            project_type = get_object_or_404(ProjectType, id=project_type_id)
            phone_code = get_object_or_404(PhoneCode, id=Phone_number_code)
            incentive_type = get_object_or_404(IncentiveType, id=incentive_type_id)
            incentive_currency_type = get_object_or_404(Incentive_Currency_Type, id=incentive_currency_type_id)
            company_currency_type_value = get_object_or_404(Currency_Type, id=company_revenue_currency_type_value)
            
            # Update the Respondent instance
            respondent_obj.name = respondent_name
            respondent_obj.middle_name = middle_name
            respondent_obj.last_name = last_name
            respondent_obj.custom_user = custom_user_obj
            respondent_obj.respondent_email = email
            respondent_obj.respondent_phone = phone_number
            respondent_obj.phone_code = phone_code
            respondent_obj.job = job_title
            respondent_obj.company_name = company_name
            respondent_obj.company_revenue = company_revenue_value
            respondent_obj.currency_type = company_currency_type_value
            respondent_obj.country = country
            respondent_obj.industry_sub_cate = industry
            respondent_obj.analyst = analyst_name 
            respondent_obj.project_name = project_name
            respondent_obj.project_code = project_code
            respondent_obj.project_type = project_type
            respondent_obj.incentive_amount = incentive_amount
            respondent_obj.incentive_code = incentive_code_name
            respondent_obj.incentive_currency_type = incentive_currency_type
            respondent_obj.incentive_type_id = incentive_type
            respondent_obj.client_name = client_name
            respondent_obj.interview_date = interview_date
            respondent_obj.interview_duration_hours = interview_duration_hours
            respondent_obj.interview_duration_minutes = interview_duration_minutes
            respondent_obj.linkdin_profile = linkdin_profile
            respondent_obj.is_active = False
            respondent_obj.save()

            messages.success(request, 'Form Submitted Successfully', extra_tags="alert-success")
            return redirect('/userdata')

        except Exception as e:
            messages.error(request, f'Error: {e}', extra_tags="alert-danger")
            return redirect(f'/edit_respondent/{id}')

    return render(request, "novusapp/edit_user_dashboard.html", context)



@login_required
@role_required(allowed_roles=['HOD'])
def userhod_data(request):
    if request.session.has_key('currentuser_id'):
        userid = request.session['currentuser_id']
        name = CustomUser.objects.get(id=userid).username
        hodname = CustomUser.objects.get(id=userid).hod_name
        hodemail = CustomUser.objects.get(id=userid).email
       
        ''' Retrieve the 'type' parameter from the GET request '''
        data_type = request.GET.get('type')
        download = request.GET.get('info')
        

        ''' Default queryset '''
        respondents = Respondent.objects.filter(hod_email=hodemail, is_active__in=[0,1]).all()

        if download == 'download':
            if data_type == 'self':
                return download_excel(respondents)
            elif data_type == 'all':
                respondents = Respondent.objects.filter(Q(hod_email=hodemail, is_active=1) | Q(is_active=1)).all()
                return download_excel(respondents)
        else:
            if data_type == 'all':
                respondents = Respondent.objects.filter(Q(hod_email=hodemail, is_active=1) | Q(is_active=1)).all()
            elif data_type == 'self':
                pass  # Respondents already filtered by default queryset

            context = {
                'respondents': respondents,
                'name': name,
                
            }

            return render(request, "novusapp/userhod_data.html", context)

    return HttpResponse('Please Login')




def autocomplete(request):
    if 'term' in request.GET:
        terms = request.GET.get('term').split(',')
        ''' Get the last term after the last comma '''
        term = terms[-1].strip()  

        qs = Industry.objects.filter(name__icontains=term)
        titles = [product.name for product in qs]
        
        return JsonResponse(titles, safe=False)
    
    return render(request, 'novusapp/userhod_data.html')


def autocomplete1(request):
    if 'term' in request.GET:
        terms = request.GET.get('term').split(',')
        ''' Get the last term after the last comma '''
        term = terms[-1].strip()  

        qs = Country.objects.filter(name__icontains=term)
        titles = [product.name for product in qs]

        return JsonResponse(titles, safe=False)
    
    return render(request, 'novusapp/userhod_data.html')


def autocomplete2(request):
    if 'term' in request.GET:
        terms = request.GET.get('term').split(',')
        ''' Get the last term after the last comma '''
        term = terms[-1].strip()  

        qs = Job.objects.filter(title__icontains=term)
        titles = [product.title for product in qs]

        return JsonResponse(titles, safe=False)
    
    return render(request, 'novusapp/userhod_data.html')





@login_required
@role_required(allowed_roles=['HOD'])
def hod_dashboard(request):
    role = RoleMaster.objects.all().values('name')
    team_manager = Manager.objects.all().values('name')

    if request.session.has_key('currentuser_id'):
        currentid =  request.session['currentuser_id']

        customuserdata = CustomUser.objects.filter(id=currentid).values('hod_name')
        print(customuserdata)

        current_hod = (customuserdata[0]['hod_name'])
        print("***************",current_hod)

        complex_obj = Register.objects.filter(is_active=0,hod_name=current_hod).values('id','username', 'email', 'password', 'hod_name','is_active')
        complex_obj1 = Register.objects.filter(hod_name=current_hod).values('id', 'email', 'password', 'hod_name','is_active','role','user_manager','username')
       
        total_user = complex_obj.count()

        ''' Create a list of dictionaries to store user-specific data '''
        user_data_list = []
        user_data_list1 = []
        

        for userdata in complex_obj:
            id = signing.dumps(userdata['id'])
            user_data = {
                'id': id,
                'username': userdata['username'],
                'email': userdata['email'],
                'password': userdata['password'],
                'hod_name': userdata['hod_name'],
                'is_active': userdata['is_active']
                
            }
            user_data_list.append(user_data)

        for userdata1 in complex_obj1:
            id = signing.dumps(userdata1['id'])
            user_data1 = {
                'id': id,
                'username': userdata1['username'],
                'email': userdata1['email'],
                'password': userdata1['password'],
                'hod_name': userdata1['hod_name'],
                'is_active': userdata1['is_active'],
                'role' : userdata1['role'],
                'team': userdata1['user_manager']
               
            }
            user_data_list1.append(user_data1)


        context = {
            'total': total_user,
            'user_data_list': user_data_list,
            'user_data_list1': user_data_list1,
            'hod':current_hod,
            'role':role,
            'team' : team_manager,
        }
        
        return render(request, "novusapp/tables.html", context)

    return HttpResponse('Please login')


def logout_view(request):
    ''' Clear the user's session '''
    logout(request)
    return redirect('/')  # Redirect to the login page or any other desired page

@login_required
@role_required(allowed_roles=['HOD'])
def tables(request):
    role = RoleMaster.objects.all().values('name')
    team = TeamLead.objects.all().values('name')

    if request.session.has_key('currentuser_id'):
        currentid =  request.session['currentuser_id']
    
        customuserdata = CustomUser.objects.filter(id=currentid).values('hod_name')

        current_hod = (customuserdata[0]['hod_name'])
        
        complex_obj = Register.objects.filter(is_active=0,hod_name=current_hod).values('id', 'email', 'password', 'hod_name')
        
        total_user = complex_obj.count()

        ''' Create a list of dictionaries to store user-specific data '''
        user_data_list = []

        for userdata in complex_obj:
            user_data = {
                'id': userdata['id'],
                'email': userdata['email'],
                'password': userdata['password'],
                'hod_name': userdata['hod_name'],
            }
            user_data_list.append(user_data)

        context = {
            'total': total_user,
            'user_data_list': user_data_list,
            'hod':current_hod,
            'role':role,
            'team' : team,
            'host_url' : host_url,
        }
        
        return render(request,'novusapp/tables.html',context)
    
    return HttpResponse('Please Login')




@login_required
@role_required(allowed_roles=['AM/Manager'])
def manager(request):
    if request.session.has_key('currentuser_id'):
        userid = request.session['currentuser_id']
        name = CustomUser.objects.get(id=userid).username
        current_manager = CustomUser.objects.get(id=userid).user_manager
        current_manager_email = CustomUser.objects.get(id=userid).email

        data_type = request.GET.get('type')
        download = request.GET.get('info')
      
        
        # Default queryset
        if data_type == 'self':
            respondents = Respondent.objects.filter(user_manager_email=current_manager_email, is_active__in=[0, 1]).all()
        elif data_type == 'all':
            respondents = Respondent.objects.filter(Q(user_manager_email=current_manager_email, is_active=1) | Q(is_active=1)).all()
        else:
            respondents = Respondent.objects.filter(user_manager_email=current_manager_email, is_active__in=[0, 1]).all()

        if download == 'download':
            if data_type == 'self':
                return download_excel(respondents)
            elif data_type == 'all':
                respondents = Respondent.objects.filter(Q(user_manager_email=current_manager_email, is_active=1) | Q(is_active=1)).all()
                return download_excel(respondents)
        else:
            if data_type == 'all':
                respondents = Respondent.objects.filter(Q(user_manager_email=current_manager_email, is_active=1) | Q(is_active=1)).all()
            elif data_type == 'self':
                pass  # Respondents already filtered by default queryset
            
          
            context = {
                'respondents': respondents,
                'name': name,
                'hod': current_manager,
           
            }

            return render(request, "novusapp/teamlead_data.html", context)

    return HttpResponse('Please Login')


@login_required
@role_required(allowed_roles=['AM/Manager'])
def managerteam_data(request):
    if request.session.has_key('currentuser_id'):
        ''' Retrieve all data from the Respondent table '''
        userid = request.session['currentuser_id']
        name = CustomUser.objects.get(id=userid).username
        useremail = CustomUser.objects.get(id=userid).email
        respondents = Respondent.objects.filter(user_manager_email=useremail,is_active=0).all()

        context = {
            'respondents':respondents,
            'name':name,
            'host_url' : host_url
        }

        return render(request,"novusapp/managerdata.html",context)

    return HttpResponse('Please Login')

@login_required
@role_required(allowed_roles=['AM/Manager'])
def form_approved(request,id):
    Respondent.objects.filter(id=id).update(is_active=1)
    return redirect('manager')


def profile(request):
    try:
        dep = Department.objects.all()
 
        if 'currentuser_id' in request.session:
            id = request.session['currentuser_id']
            profile_obj = CustomUser.objects.get(id=id)
            print(profile_obj.profile_picture)
            if request.method == 'POST':
                mobile = request.POST.get('mobile_no')
                dept = request.POST.get('department')
                profile_picture = request.FILES.get('profile_picture')
                print('$$$$$$$$$$$', profile_picture)
                
                if not dept:
                    messages.error(request, 'Please choose a department.', extra_tags="alert-danger")
                    return redirect('/profile')
                    
                try:
                    dept_obj = Department.objects.get(id=dept)
                except Department.DoesNotExist:
                    messages.error(request, 'Department does not exist.', extra_tags="alert-danger")
                    return redirect('/profile')
 
                if CustomUser.objects.filter(id=id, dep=dept, mobile=mobile).exists():
                    messages.info(request, 'Same record already exists.', extra_tags="alert-warning")
                    return redirect('/profile')
 
                CustomUser.objects.filter(id=id).update(dep=dept, mobile=mobile, profile_picture=profile_picture)
                
                # Update related Respondent information
                tl_email = profile_obj.email
                Respondent.objects.filter(email=tl_email).update(Department=dept_obj.name)
                
                messages.success(request, 'Profile updated successfully.', extra_tags="alert-success")
                return redirect('/profile')
 
            context = {
                'profile_obj': profile_obj,
                'department': dep,
            }
            return render(request, "novusapp/edit.html", context)
 
        return HttpResponse('Please Login')
 
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}', extra_tags="alert-danger")
        return render(request, "novusapp/edit.html", {'department': dep})
 


def change_password(request):
    ''' Get the user ID from the session '''
    userid = request.session.get('currentuser_id')
    role = CustomUser.objects.get(id=userid).role
    name = CustomUser.objects.get(id=userid).username
    if request.method == 'POST':
        ''' Get the old, new, and confirmed passwords from the form '''
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        
        
       
        ''' Retrieve the user object from the database '''
        user = CustomUser.objects.get(id=userid)

        ''' Check if the old password matches the user's current password '''
        if not check_password(old_password, user.password):
            messages.error(request, 'Old password is incorrect',extra_tags="alert-danger")
            return redirect('/profile/change_password')  
        
        if old_password == new_password:
            messages.warning(request,"Old and new password same please change this password.", extra_tags="alert-warning")
            return redirect("/profile/change_password")


        user.set_password(new_password)
        user.save()

        messages.success(request, 'Password changed successfully',extra_tags="alert-success")
        return redirect('/') 

    context = {
        'role':role,
        'username':name}
    return render(request, 'novusapp/change_password.html',context)  


''' login templates render '''

def loginDemo(request):
    return render(request, 'novusapp/base1.html')


def logout_view(request):
    logout(request)
    return redirect('/')



def send_email(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            # Generate a unique token for the user
            token = str(uuid.uuid4())
            print('token kdsfjkdfjf', token)
            # Get the user object associated with the provided email
            user = UserModel.objects.get(email=email)
            # Update the user's token
            user.token = token
            user.save()
 
            # Render the HTML email content
            ctx = {
                'token': token
            }
            msg_html = render_to_string('novusapp/password_reset_form.html', ctx)
            plain_message = strip_tags(msg_html)
            recipient_list = [user.email]
 
            # Send the password reset email
            subject = 'Request for password reset.'
            to_mail = user.email
            from_mail = "noreply.erp@unimrkt.com"
            send_mail (
                subject,
                plain_message,
                from_mail,
                [to_mail],
                recipient_list,
                html_message=msg_html,
            )
 
            # Notify the user that the password reset link has been sent
            messages.success(request, "Password reset link has been sent to your email.", extra_tags="alert-success")
            return redirect('/')
        
        except UserModel.DoesNotExist:
            # If the provided email does not exist in the system, display an error message
            messages.error(request, "This email does not exist in our system.", extra_tags="alert-danger")
            return render(request, "novusapp/send_email.html")
 
    # If the request method is not POST or if there's any other error, render the send_email.html template
    return render(request, "novusapp/send_email.html")
 
 
def reset_password_view(request, token):
    if token:
        try:
            user = UserModel.objects.filter(token=token).first()
            if user:
                # Check if the token is expired (optional)
                if user.updated_at < timezone.now() - timezone.timedelta(minutes=10):
                    raise ValueError('The link to reset your password has expired. Please request a new one.')
 
                if request.method == "POST":
                    password = request.POST.get('password')
                    password2 = request.POST.get('password2')
                    if password != password2:
                        messages.error(request, "Passwords do not match.", extra_tags="alert-danger")
                        return redirect(f'/reset-password/{token}')
                    
                    # Update the password and clear the token
                    user.set_password(password)
                    user.token = None
                    user.save()
                    messages.success(request, "Password reset successfully.",extra_tags="alert-success")
                    return redirect('/')  # Redirect to login page or any other page
                context = {'token': token}
                return render(request, "novusapp/reset_password.html", context)
            else:
                return HttpResponse('User not found.')
        except ValueError as e:
            messages.error(request, str(e), extra_tags="alert-danger")
            return redirect('/')
    else:
        return HttpResponse('Token not provided.')






@login_required
@role_required(allowed_roles=['AM/Manager'])
def sendremark(request, userid, respondentid):
    print('Remark Getting')
    try:
        if request.session.has_key('currentuser_id'):
            if request.method == "POST":
                remark_comment = request.POST.get('remark')
                Respondent.objects.filter(id=respondentid, custom_user=userid).update(remark=remark_comment)
                messages.success(request, 'Remark sent successfully', extra_tags="alert-success")
                return redirect('/managerteam_data')
    except Exception as e:
        messages.error(request, f'Error: {e}', extra_tags="alert-danger")
    return redirect('/managerteam_data')



@login_required
@role_required(allowed_roles=['Team Lead'])
def user_excel_data(request):
    if request.session.has_key('currentuser_id'):
        userid = request.session['currentuser_id']
        custom_user_obj = CustomUser.objects.get(id=userid)
        TeamLeadname = custom_user_obj.username
        TeamLead_email = custom_user_obj.email
        user_manager = custom_user_obj.user_manager
        department = getattr(custom_user_obj.dep, 'name', "")

        try:
            hod_name = custom_user_obj.hod_name
        except Exception:
            messages.error(request, "Your Registration is not confirmed. Please wait some time and try again later.", extra_tags="alert-danger")
            return redirect('/')

        try:
            hod_email = Hod.objects.filter(name=hod_name)[0].email
        except Exception as e:
            messages.error(request, f"{e}", extra_tags="alert-danger")

        user_manager_email = ''
        if user_manager:
            try:
                user_manager_email = Manager.objects.get(name=user_manager).email
            except Manager.DoesNotExist:
                user_manager_email = TeamLead_email
        else:
            user_manager_email = TeamLead_email

        if request.method == 'POST':
            if 'excel_file' in request.FILES:
                excel_file = request.FILES['excel_file']
                fs = FileSystemStorage()
                filename = fs.save(excel_file.name, excel_file)
                uploaded_file_url = fs.url(filename)

                try:
                    # Read the uploaded Excel file
                    df = pd.read_excel(fs.path(filename), sheet_name='Respondent Incentive Sheet')

                    for index, row in df.iterrows():
                        try:
                            respondent_name = row['Respondent Name']
                            middle_name = row.get('Middle Name', '')
                            last_name = row.get('Last Name', '')
                            company_name = row.get('Company', '')
                            industry_name = row.get('Industry', '')
                            industry_sub_cate_name = row.get('Industry Sub Cate', '')
                            job_title = row.get('Designation', '')
                            phone_number = row.get('Contact', '')
                            phone_code_value = row.get('Phone_number_code', '')
                            email = row['Email id']
                            respondent_email = row.get('Respondent Email', '')
                            country_name = row['Country']
                            project_name = row.get('Project Name', '')
                            project_type_name = row['Project Type']
                            project_code = row.get('PCR Code', '')
                            client_name = row.get('Client Name', '')
                            interview_duration_minutes = row.get('Interview Duration Minutes', '')
                            interview_duration_hours = row.get('Interview Duration Hours', '')
                            interview_date = row.get('Date of Interview', '')
                            incentive_code = row.get('Incentive Code', '')
                            incentive_amount = row.get('Incentive', '')
                            incentive_type_name = row.get('Incentive Type', '')
                            incentive_currency_type_name = row.get('Incentive Currency Type', '')
                            paypal_id_amazon_voucher = row.get('Paypal Id/ Amazon Voucher', '')
                            analyst_name = row.get('Scheduled by', '')
                            company_revenue = row.get('Company Revenue', '')
                            company_revenue_currency_type_name = row.get('Company Revenue Currency Type', '')
                            linkdin_profile = row.get('Linkdin Profile', '')
                         
                         

                            # Handle ProjectType retrieval
                            try:
                                project_type = ProjectType.objects.get(name=project_type_name)
                            except ProjectType.DoesNotExist:
                                messages.error(request, f"Error processing row {index + 1}: ProjectType '{project_type_name}' does not exist.", extra_tags="alert-danger")
                                continue

                            # Handle IncentiveType retrieval
                            try:
                                incentive_type = IncentiveType.objects.get(name=incentive_type_name)
                            except IncentiveType.DoesNotExist:
                                messages.error(request, f"Error processing row {index + 1}: IncentiveType '{incentive_type_name}' does not exist.", extra_tags="alert-danger")
                                continue

                            # Handle IncentiveCurrencyType retrieval
                            try:
                                incentive_currency_type = Incentive_Currency_Type.objects.get(currency_type=incentive_currency_type_name)
                            except Incentive_Currency_Type.DoesNotExist:
                                messages.error(request, f"Error processing row {index + 1}: Incentive Currency Type '{incentive_currency_type_name}' does not exist.", extra_tags="alert-danger")
                                continue

                            # Handle Currency_Type retrieval
                            try:
                                currency_type = Currency_Type.objects.get(currency_type=company_revenue_currency_type_name)
                            except Currency_Type.DoesNotExist:
                                messages.error(request, f"Error processing row {index + 1}: Currency Type '{company_revenue_currency_type_name}' does not exist.", extra_tags="alert-danger")
                                continue

                            # Fetch or create related objects
                            with transaction.atomic():
                                country, _ = Country.objects.get_or_create(name=country_name)
                                phone_code, _ = PhoneCode.objects.get_or_create(phone_code=phone_code_value)
                                industry_sub_cate, _ = Industry_Sub_Cate.objects.get_or_create(name=industry_name)

                                # Create or update the Respondent instance
                                respondent = Respondent.objects.create(
                                        respondent_email = respondent_email,
                                        name = respondent_name,
                                        middle_name = middle_name,
                                        last_name = last_name,
                                        custom_user = custom_user_obj,
                                        job = job_title,
                                        email =  email,
                                        respondent_phone = phone_number,
                                        phone_code = phone_code,
                                        currency_type = currency_type,
                                        analyst = analyst_name,
                                        project_name = project_name,
                                        project_type = project_type,
                                        project_code = project_code,
                                        incentive_code = incentive_code,
                                        incentive_type_id = incentive_type,
                                        incentive_amount = incentive_amount,
                                        incentive_currency_type = incentive_currency_type,
                                        country = country,
                                        industry_sub_cate = industry_sub_cate,
                                        company_name = company_name,
                                        company_revenue = company_revenue,
                                        client_name = client_name,
                                        interview_duration_hours = interview_duration_hours,
                                        interview_duration_minutes = interview_duration_minutes,
                                        interview_date = interview_date,
                                        linkdin_profile = linkdin_profile,
                                        team_lead = TeamLeadname,
                                        Department = department,
                                        user_manager = user_manager,
                                        user_manager_email = user_manager_email,
                                        hod_email = hod_email,
                                        payment_id = paypal_id_amazon_voucher,
                                        is_active = False 
                                )

                        except Exception as e:
                            messages.error(request, f"Error processing row {index + 1}: {e}", extra_tags="alert-danger")

                    messages.success(request, 'Excel file processed successfully', extra_tags="alert-success")
                    return redirect('/user_dashboard')

                except Exception as e:
                    messages.error(request, f"Error reading Excel file: {e}", extra_tags="alert-danger")
                    return redirect('/user_dashboard')

            else:
                messages.error(request, 'No file uploaded', extra_tags="alert-danger")
                return redirect('/user_dashboard')

        return render(request, "novusapp/user_dashboard.html")

    return HttpResponse('Please login')



############################################################### Payment Views ################################################

@login_required
@role_required(allowed_roles=['HOD'])
def payment_page(request):
    if request.session.has_key('currentuser_id'):
        userid = request.session['currentuser_id']
        name = CustomUser.objects.get(id=userid).username
        hodname = CustomUser.objects.get(id=userid).hod_name
        hodemail = CustomUser.objects.get(id=userid).email
       
        ''' Retrieve the 'type' parameter from the GET request '''
        data_type = request.GET.get('type')
        download = request.GET.get('info')
        items_per_page = int(request.GET.get('items_per_page', 10))

        ''' Default queryset '''
        respondents = Respondent.objects.filter(hod_email=hodemail, is_active__in=[0,1]).all()

        if download == 'download':
            if data_type == 'self':
                return download_excel(respondents)
            elif data_type == 'all':
                respondents = Respondent.objects.filter(Q(hod_email=hodemail, is_active=1) | Q(is_active=1)).all()
                return download_excel(respondents)
        else:
            if data_type == 'all':
                respondents = Respondent.objects.filter(Q(hod_email=hodemail, is_active=1) | Q(is_active=1)).all()
            elif data_type == 'self':
                pass  # Respondents already filtered by default queryset

            ''' Paginator '''
            paginator = Paginator(respondents, items_per_page)
            page_number = request.GET.get('page')

            try:
                servicedatafinal = paginator.page(page_number)
            except PageNotAnInteger:
                servicedatafinal = paginator.page(1)
            except EmptyPage:
                servicedatafinal = paginator.page(paginator.num_pages)

            ''' Get total page count for pagination links '''
            totalpage = servicedatafinal.paginator.num_pages
            totalpagelist = [i + 1 for i in range(totalpage)]

            ''' Create the URL for pagination links '''
            base_url = reverse('userhod_data')
            pagination_url = f"{base_url}?type={data_type}&items_per_page={items_per_page}&page="

            context = {
                'respondents': servicedatafinal,
                'name': name,
                'lastpage': totalpage,
                'totalpagelist': totalpagelist,
                'items_per_page': items_per_page,
                'pagination_url': pagination_url,  
            }

            return render(request, 'novusapp/hod_payment.html', context)

    return HttpResponse('Please Login')



@login_required
@role_required(allowed_roles=['HOD'])
def process_payment(request, pk):
    if request.method == "POST":
        get_payment_mode = request.POST.get('payment_mode')
        respondent = Respondent.objects.get(id=pk)
        payment_id = respondent.payment_id
        print(get_payment_mode)      
        if not respondent.incentive_type == get_payment_mode:
           messages.error(request, "Please select correct payment mode.", extra_tags='alert-error')
           return redirect('/payment-page/')
       
       
        if respondent.pay_status == True:
           messages.error(request, "Payment for this client has already been completed.", extra_tags='alert-error')
           return redirect('/payment-page/')
       
        if payment_id:
            if get_payment_mode == "paypal":
                host = request.get_host()
                    
                    # Constructing return_url with custom data
                return_url = 'http://{}{}?{}'.format(
                        host, reverse('payment_done'), urlencode({'respondent_id': respondent.id})
                    )
                    
                paypal_dict = {
                        'business': str(payment_id),
                        'amount': str(respondent.incentive),
                        'currency_code': 'USD',
                        'item_name': 'Payment for {}'.format(respondent),
                        'invoice': str(uuid.uuid4()),
                        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
                        'return_url': return_url,
                        'cancel_return': 'http://{}{}'.format(host, reverse('payment_cancelled')),
                        'custom': '{}_{}'.format(respondent.id, payment_id),  # Combine respondent ID and payment ID
                    }
                respondent.payment_mode=get_payment_mode
                respondent.save()
                form = PayPalPaymentsForm(initial=paypal_dict)
                return render(request, 'novusapp/paypal/process_payment.html', {'form': form})
                
            elif get_payment_mode == "Xoxo Day":
                return get_vouchers()
                
            
        else:
            messages.error(request, 'Payment ID does not exist.', extra_tags='alert-error')

    respondent_obj = Respondent.objects.filter(id=pk)
    context = {
        'respondents': respondent_obj
    }
    return render(request, 'novusapp/paypal/payment_mode.html', context)



import requests
def xoxo_login(request):
    if request.method == "POST":
        email_id_or_mobile =request.POST.get('email')
        print(email_id_or_mobile)
        
    
    return render(request, 'novusapp/xoxo/xoxo_login.html')     



@csrf_exempt
def payment_done(request):
    custom_data = request.GET.get('respondent_id')
    
    if custom_data:
        try:
            respondent = Respondent.objects.get(id=custom_data)
            respondent.pay_status = 1
            respondent.save()
            messages.success(request, 'Payment successfully completed for Respondent {}.'.format(custom_data), extra_tags='alert-success')
            return redirect('/payment-page/')
        except Respondent.DoesNotExist:
            return HttpResponseBadRequest("Invalid respondent ID")
    else:
        return HttpResponseBadRequest("No custom data found in the request")


@csrf_exempt
def payment_cancelled(request):
    # This view is called when payment is cancelled
    messages.warning(request, 'Payment cancelled.')
    return redirect('/payment-page/')


import requests
from django.conf import settings
def process_xoxo_day_payment(request):
    # Replace these placeholders with actual Xoxo Day API endpoint and authentication details
    xoxo_day_api_url = 'https://stagingaccount.xoxoday.com/chef/v1/oauth/token'
    url = 'https://stagingaccount.xoxoday.com/login'
    xoxo_day_client_id = settings.XOXO_CLIENT_ID
    xoxo_day_secert_kay = settings.XOXO_SECERT_ID
    
    # Construct payload for Xoxo Day API
    payload = {
 
        # Add any other required parameters
    }
    
    #token = obtain_xoxo_day_token(xoxo_day_client_id, xoxo_day_secret_key)
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.post(xoxo_day_api_url)
    print(response.text)
    
    return HttpResponse(response)



from django.shortcuts import render

def voucher_dropdown_view(request):
    return render(request, 'novusapp/xoxo/vouchers.html')


def place_order(request):
    phone_code = PhoneCode.objects.all().values('id', 'phone_code')
    
    context = {
        'phone_code': phone_code,
    }
    return render(request, 'novusapp/xoxo/place_order.html',context)
