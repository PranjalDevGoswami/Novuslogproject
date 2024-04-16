# Create your views here.
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import (
    CustomUser, Hod, Register, TeamLead, RoleMaster, Respondent,
    Job, Country, Industry, Company, Analyst, Project, Incentive,
    ProjectInterview, Manager, Department, Currency_Type,ProjectType,
    IncentiveType,PhoneCode,PhoneNumber,Industry_Sub_Cate
)
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

import io
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
    # Create an in-memory output stream for storing Excel file
    output = io.BytesIO()
    
    # Create a new workbook
    wb = Workbook()
    ws = wb.active
    # Set the height of the header row
    ws.row_dimensions[1].height = 22  # Set height in points (1 point = 1/72 inch)
    # Write headers with colors and filter
    headers = ['Respondent Name', 'Email', 'Phone Number', 'Job Title', 'Company', 'Country', 'Industry', 'Interviewer Name', 'Project', 'Project Type', 'Company Revenue', 'Incentive', 'Interview Duration', 'Interview Date', 'Team Lead', 'Manager', 'Department', 'Status']
    for idx, header in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=idx, value=header)
        # Apply color to the header cell
        cell.fill = PatternFill(start_color="FFCCCB", end_color="FFCCCB", fill_type="solid")
        # Enable filtering for each column
        ws.auto_filter.ref = ws.dimensions
    
    # Write data rows
    for respondent in respondents:
        row = [
            respondent.name + ' ' + (respondent.middle_name if respondent.middle_name else '') + ' ' + (respondent.last_name if respondent.last_name else ''),
            respondent.respondent_email,
            respondent.respondent_phone.phone_code + ' ' + respondent.respondent_phone.phone_number,
            respondent.job.title,
            respondent.company.name,
            respondent.country.name,
            respondent.industry.name,
            respondent.analyst.title,
            respondent.project.name,
            respondent.project.project_type.name if respondent.project.project_type else '',  # Convert ProjectType to string
            respondent.company.revenue + ' ' + respondent.company.revenue_currency_type if respondent.company.revenue != "0" else '',
            respondent.incentive.Unique_identifier + ' ' + respondent.incentive.incentive_currency_type,
            str(respondent.project_interview.interview_duration_hours) + 'hr:' + str(respondent.project_interview.interview_duration_minutes) + 'min',
            respondent.project_interview.interview_date,
            respondent.team_lead if respondent.team_lead else '',
            respondent.user_manager if respondent.user_manager else '',
            respondent.Department if respondent.Department else '',
            'Pending' if respondent.is_active == 0 else 'Complete'
        ]
        ws.append(row)
    
    # Save workbook to the output stream
    wb.save(output)
    output.seek(0)
    
    # Set response headers for serving Excel file
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
        TeamLeadname = CustomUser.objects.get(id=userid).username
        TeamLead_email = CustomUser.objects.get(id=userid).email
        user_manager = CustomUser.objects.get(id=userid).user_manager
        custom_user_obj = CustomUser.objects.get(id=userid)
        try:
            department_obj = get_object_or_404(CustomUser, id=int(userid))
            department = department_obj.dep.name
        except:
            department = ""
        try:
            hod_name = CustomUser.objects.get(id=userid).hod_name
        except Exception as e:
            messages.error(request, "Your Registration is not confirmed please wait some time and after login.", extra_tags="alert-danger")
            return redirect('/')
        try:
            hod_email = Hod.objects.get(name=hod_name).email
        except Exception as e:
            messages.error(request, f"{e}", extra_tags="alert-danger")

        if user_manager == '':
            user_manager_email = CustomUser.objects.get(id=userid).email
        else:
            try:
                user_manager_email = Manager.objects.get(name=user_manager).email
            except:
                pass

        industries = Industry.objects.all()
        industry_data = {industry: industry.subindustry.all() for industry in industries if industry.subindustry.exists()}

        mycountry = Country.objects.values('name').distinct()
        currency_type = Currency_Type.objects.all().values('currency_type')
        Project_Type = ProjectType.objects.all().values('id', 'name')
        Incentive_Type = IncentiveType.objects.all().values('id', 'name')
        phone_code = PhoneCode.objects.all().values('id', 'phone_code')

        if request.method == 'POST':
            try:
                ''' Get the data from the POST request '''
                respondent_name = request.POST.get('respondent_name')
                middle_name = request.POST.get('middle_name')
                last_name = request.POST.get('last_name')
                email = request.POST.get('email')
                job_title = request.POST.get('job_title')
                country_name = request.POST.get('country')
                phone_number = request.POST.get('phone_number')
                Phone_number_code = request.POST.get('Phone_number_code')
                industry_name = request.POST.get('industry')
                company_name = request.POST.get('company')
                company_revenue_value = request.POST.get('company_revenue')
                company_revenue_currency_type_value = request.POST.get('company_revenue_currency_type')
                analyst_name = request.POST.get('analyst')
                project_type_id = request.POST.get('project_type')
                project_name = request.POST.get('project')
                project_code = request.POST.get('project_code')
                interview_duration_hours = request.POST.get('interview_duration_hours')
                interview_duration_minutes = request.POST.get('interview_duration_minutes')
                interview_date = request.POST.get('interview_date')
                incentive_type_id = request.POST.get('incentive_type')
                incentive_name = request.POST.get('incentive')
                incentive_code = request.POST.get('incentive_code')
                incentive_currency_type = request.POST.get('incentive_currency_type')
                linkdin_profile = request.POST.get('linkdin_profile')
              
                
                
                if not company_revenue_value:
                    company_revenue_value = 0

                if not company_revenue_currency_type_value:
                    company_revenue_currency_type_value = ""

                ''' Create or retrieve related records from other tables '''
                try:
                    job = Job.objects.create(title=job_title)
                except Exception as e:
                    messages.error(request, f"Error creating job: {e}", extra_tags="alert-danger")
                    return redirect('/user_dashboard')

                try:
                    country = Country.objects.create(name=country_name)
                except Exception as e:
                    messages.error(request, f"Error creating country: {e}", extra_tags="alert-danger")
                    return redirect('/user_dashboard')

                try:
                    phone = PhoneNumber.objects.create(phone_number=phone_number, phone_code=Phone_number_code)
                except Exception as e:
                    messages.error(request, f"Error creating phone number: {e}", extra_tags="alert-danger")
                    return redirect('/user_dashboard')

                try:
                    industry = Industry.objects.create(name=industry_name)
                except Exception as e:
                    messages.error(request, f"Error creating industry: {e}", extra_tags="alert-danger")
                    return redirect('/user_dashboard')

                try:
                    company = Company.objects.create(name=company_name, revenue=company_revenue_value, revenue_currency_type=company_revenue_currency_type_value)
                except Exception as e:
                    messages.error(request, f"Error creating company: {e}", extra_tags="alert-danger")
                    return redirect('/user_dashboard')

                try:
                    analyst = Analyst.objects.create(title=analyst_name)
                except Exception as e:
                    messages.error(request, f"Error creating analyst: {e}", extra_tags="alert-danger")
                    return redirect('/user_dashboard')

                try:
                    project_type_obj = get_object_or_404(ProjectType, pk=project_type_id)
                except ProjectType.DoesNotExist:
                    messages.error(request, "Project type not found", extra_tags="alert-danger")
                    return redirect('/user_dashboard')

                try:
                    project = Project.objects.create(name=project_name, project_type=project_type_obj,project_code=project_code)
                except Exception as e:
                    messages.error(request, f"Error creating project: {e}", extra_tags="alert-danger")
                    return redirect('/user_dashboard')

                try:
                    project_interview = ProjectInterview.objects.create(project=project, interview_duration_hours=interview_duration_hours, interview_duration_minutes=interview_duration_minutes, interview_date=interview_date)
                except Exception as e:
                    messages.error(request, f"Error creating project interview: {e}", extra_tags="alert-danger")
                    return redirect('/user_dashboard')

                try:
                    incentives_type_obj = get_object_or_404(IncentiveType, pk=incentive_type_id)
                except IncentiveType.DoesNotExist:
                    messages.error(request, "Incentive type not found", extra_tags="alert-danger")
                    return redirect('/user_dashboard')

                try:
                    incentive = Incentive.objects.create(project=project, Unique_identifier=incentive_name, incentive_code=incentive_code, incentive_type=incentives_type_obj, incentive_currency_type=incentive_currency_type)
                except Exception as e:
                    messages.error(request, f"Error creating incentive: {e}", extra_tags="alert-danger")
                    return redirect('/user_dashboard')

                ''' Create the Respondent instance and associate it with the related records '''
                respondent = Respondent.objects.create(
                    name=respondent_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    respondent_email=email,
                    custom_user=custom_user_obj,
                    respondent_phone=phone,
                    job=job,
                    email=TeamLead_email,
                    user_manager=user_manager,
                    hod_email=hod_email,
                    user_manager_email=user_manager_email,
                    country=country,
                    industry=industry,
                    company=company,
                    analyst=analyst,
                    project=project,
                    incentive=incentive,
                    linkdin_profile=linkdin_profile,
                    project_interview=project_interview,
                    team_lead=TeamLeadname,
                    Department=department,
                    is_active=0
                )

                ''' Save the Respondent instance to the database '''
                respondent.save()
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
        }

        return render(request, "novusapp/user_dashboard.html", context)

    return HttpResponse('Please login')




@login_required
@role_required(allowed_roles=['Team Lead'])
def userdata(request):
    if request.session.has_key('currentuser_id'):
        userid = request.session['currentuser_id']
        name = CustomUser.objects.get(id=userid).username
        useremail = CustomUser.objects.get(id=userid).email

        data_type = request.GET.get('type')
        download = request.GET.get('info')
        items_per_page = int(request.GET.get('items_per_page', 10))
        
        # Default queryset
        respondents = Respondent.objects.filter(email=useremail, is_active__in=[0,1]).all()

        if download == 'download':
            if data_type == 'self':
                return download_excel(respondents)
            elif data_type == 'all':
                respondents = Respondent.objects.filter(Q(email=useremail, is_active=1) | Q(is_active=1)).all()
                return download_excel(respondents)
        else:
            if data_type == 'all':
                respondents = Respondent.objects.filter(Q(email=useremail, is_active=1) | Q(is_active=1)).all()
            elif data_type == 'self':
                pass  # Respondents already filtered by default queryset
            # Pagination logic
            paginator = Paginator(respondents, items_per_page)
            page_number = request.GET.get('page')

            try:
                servicedatafinal = paginator.page(page_number)
            except PageNotAnInteger:
                servicedatafinal = paginator.page(1)
            except EmptyPage:
                servicedatafinal = paginator.page(paginator.num_pages)

            totalpage = servicedatafinal.paginator.num_pages
            totalpagelist = [i + 1 for i in range(totalpage)]

            base_url = reverse('userdata')
            pagination_url = f"{base_url}?type={data_type}&items_per_page={items_per_page}&page="

            context = {
                'respondents': servicedatafinal,
                'name': name,
                'lastpage': totalpage,
                'totalpagelist': totalpagelist,
                'items_per_page': items_per_page,
                'pagination_url': pagination_url, 
            }
            return render(request, "novusapp/userdata.html", context)

    return HttpResponse('Please Login')


@login_required
@role_required(allowed_roles=['Team Lead'])
def edit_respondent(request, id):
    print('###@@@@@@@@@@@@@@@@@@@@', id)
    try:
        respondent_obj = Respondent.objects.get(id=id)
    except Respondent.DoesNotExist:
        messages.error(request, 'Respondent not found', extra_tags="alert-danger")
        return redirect('/user_dashboard')

    # Fetch related data
    phone_code = PhoneCode.objects.all().values('id', 'phone_code')
    currency_type = Currency_Type.objects.all().values('currency_type')
    mycountry = Country.objects.all().values('name').distinct()
    industries = Industry.objects.all()
    industry_data = {industry: industry.subindustry.all() for industry in industries if industry.subindustry.exists()}
    Incentive_Type = IncentiveType.objects.all().values('id', 'name')
    Project_Type = ProjectType.objects.all().values('id', 'name')
    context = {
        "respondents": [respondent_obj],
        'phone_code': phone_code,
        'currency_type': currency_type,
        'allcountry': mycountry,
        'industry_data': industry_data,
        'Incentive_Type': Incentive_Type,
        'Project_Type': Project_Type,
    }

    if request.method == "POST":
        respondent_obj = Respondent.objects.get(id=id)
        print('RRRRRRRRRRRRRRRRRR', respondent_obj)
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
            project_name = request.POST.get('project')
            project_code = request.POST.get('project_code')
            project_type_id = request.POST.get('project_type')
            incentive_name = request.POST.get('incentive')
            linkdin_profile = request.POST.get('linkdin_profile')
            incentive_currency_type = request.POST.get('incentive_currency_type')
            interview_date = request.POST.get('interview_date')
            interview_duration_hours = request.POST.get('interview_duration_hours')
            interview_duration_minutes = request.POST.get('interview_duration_minutes')
          

            # Update job object if it exists
            Job.objects.filter(respondent_id=id).update(title=job_title,respondent_id=id)

            # Update country object if it exists
            Country.objects.filter(respondent_id=id).update(name=country_name,respondent_id=id)

            # Update phone object if it exists
            PhoneNumber.objects.filter(respondent_id=id).update(phone_code=Phone_number_code,respondent_id=id)

            # Update industry object if it exists
            Industry.objects.filter(respondent_id=id).update(name=industry_name,respondent_id=id)

            # Update company object if it exists
            Company.objects.filter(respondent_id=id).update(name=company_name, revenue=company_revenue_value, revenue_currency_type=company_revenue_currency_type_value,respondent_id=id)

            # Update analyst object if it exists
            Analyst.objects.filter(respondent_id=id).update(title=analyst_name,respondent_id=id)

            # Get project type object
            project_type_obj = get_object_or_404(ProjectType, pk=project_type_id)

            # Update project object if it exists
            Project.objects.filter(respondent_id=id).update(name=project_name, project_type=project_type_obj,respondent_id=id)
            
            # Get the queryset of project objects for the given respondent_id
            project_objs = Project.objects.filter(respondent_id=id)

            # Choose one project object from the queryset (you may need to define some logic here)
            project_obj = project_objs.first()  # For example, choose the first project object

            # Update project interview object if it exists
            ProjectInterview.objects.filter(respondent_id=id).update(
                project=project_obj,
                interview_duration_hours=interview_duration_hours,
                interview_duration_minutes=interview_duration_minutes,
                interview_date=interview_date,respondent_id=id
            )

            # Get incentive type object
            incentives_type_obj = get_object_or_404(IncentiveType, pk=incentive_type_id)

            # Update incentive object if it exists
            Incentive.objects.filter(respondent_id=id).update(
                project=project_obj,
                incentive_code=incentive_code,
                incentive_type_id=incentive_type_id,
                incentive_currency_type=incentive_currency_type,respondent_id=id
            )

            
            # Fetch all master objects after updating
            job_obj = Job.objects.filter(respondent_id=id).first()
            country_obj = Country.objects.filter(respondent_id=id).first()
            phone_objs = PhoneNumber.objects.filter(respondent_id=id)
            phone_obj = phone_objs.first() if phone_objs.exists() else None
            industry_obj = Industry.objects.filter(respondent_id=id).first()
            company_obj = Company.objects.filter(respondent_id=id).first()
            analyst_obj = Analyst.objects.filter(respondent_id=id).first()
            projectinterview_obj = ProjectInterview.objects.filter(respondent_id=id).first()
            incentive_obj = Incentive.objects.filter(respondent_id=id).first()


            # Update the Respondent instance
            respondent_obj.name = respondent_name
            respondent_obj.middle_name = middle_name
            respondent_obj.last_name = last_name
            respondent_obj.custom_user = custom_user_obj
            respondent_obj.job = job_obj
            respondent_obj.respondent_email = email
            respondent_obj.respondent_phone = phone_obj
            respondent_obj.country = country_obj
            respondent_obj.industry = industry_obj
            respondent_obj.company = company_obj
            respondent_obj.analyst = analyst_obj
            respondent_obj.project = project_obj
            respondent_obj.incentive_type_id = incentive_type_id  # Assigning the ID of the IncentiveType
            respondent_obj.incentive = incentive_obj
            respondent_obj.project_interview = projectinterview_obj
            respondent_obj.linkdin_profile = linkdin_profile
            respondent_obj.is_active = False
            respondent_obj.save()

            messages.success(request, 'Form Submitted Successfully', extra_tags="alert-success")
            return redirect('/userdata')

        except Exception as e:
            messages.error(request, f'Error: {e}', extra_tags="alert-danger")
            return redirect('/user_dashboard')

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

        current_hod = (customuserdata[0]['hod_name'])

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
        items_per_page = int(request.GET.get('items_per_page', 10))
        
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
            
            # Pagination logic
            paginator = Paginator(respondents, items_per_page)
            page_number = request.GET.get('page')

            try:
                servicedatafinal = paginator.page(page_number)
            except PageNotAnInteger:
                servicedatafinal = paginator.page(1)
            except EmptyPage:
                servicedatafinal = paginator.page(paginator.num_pages)

            totalpage = servicedatafinal.paginator.num_pages
            totalpagelist = [i + 1 for i in range(totalpage)]

            base_url = reverse('manager')
            pagination_url = f"{base_url}?type={data_type}&items_per_page={items_per_page}&page="

            context = {
                'respondents': servicedatafinal,
                'name': name,
                'lastpage': totalpage,
                'totalpagelist': totalpagelist,
                'hod': current_manager,
                'items_per_page': items_per_page,
                'pagination_url': pagination_url,
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

        if request.session.has_key('currentuser_id'):
            id = request.session['currentuser_id']
            profile_obj = CustomUser.objects.get(id=id)

            if request.method == 'POST':
                mobile = request.POST.get('mobile_no')
                dept = request.POST.get('department')
                try:
                    dept_obj = Department.objects.get(id=dept)
                except:
                    pass
                    
                ''' Update user information '''
                if CustomUser.objects.filter(id=id,dep=dept, mobile=mobile).exists():
                    messages.info(request, 'Same record already exists.', extra_tags="alert-warning")
                    return redirect('/profile')
                
                CustomUser.objects.filter(id=id).update(dep=dept, mobile=mobile)
                
                ''' Update related Respondent information '''
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
        ''' Handle other exceptions '''
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





