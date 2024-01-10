# Create your views here.
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser,Hod,Register,TeamLead,RoleMaster,Respondent, Job, Country, Industry, Company, Analyst, Project, Incentive, ProjectInterview,Manager,Department
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


credentials = yaml.load(open('./novusproject/credentials.yml','r'),Loader=yaml.FullLoader)
host_url = credentials['hosted_url']


# Define a list of valid email domains
VALID_EMAIL_DOMAINS = ['unimrkt.com', 'novusinsights.com']

def is_valid_email_domain(email):
    # Split the email address to get the domain part
    domain = email.split('@')[-1]

    # Check if the email is blank
    if not email:
        return False

    # Check if the domain is in the list of valid domains
    if domain in VALID_EMAIL_DOMAINS:
        return True
    return False


def register(request):
    hod = Hod.objects.filter(is_active=True).values('name')
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['pass']
        confpassword = request.POST['conf_pass']
        try:
            novus_hod = request.POST['hod']
        except:
            pass

        # Check if the email already exists
        try:
            existing_user = Register.objects.get(email=email)
            existing_in_customuser = CustomUser.objects.get(email=email)
            messages.error(request, 'This email is already registered.', extra_tags="alert-danger")
            return redirect('/register')
        except Register.DoesNotExist:
            pass

        # Check if the passwords match
        if password != confpassword:
            messages.error(request, 'Passwords do not match.',extra_tags="alert-danger")
            return redirect('register')

        # Validate email domain
        if not is_valid_email_domain(email):
            if not email:
                messages.error(request, 'Please fill in the email field.', extra_tags="alert-danger")
            else:
                messages.error(request, 'Invalid email domain. Please use a valid domain.',extra_tags="alert-danger")
            return redirect('register')
        # Create a new user
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
    role = RoleMaster.objects.filter(is_active=True).values('name')
    team_manager = Manager.objects.filter(is_active=True).values('name')
    if request.session.has_key('currentuser_id'):
        currentid =  request.session['currentuser_id']
    
        customuserdata = CustomUser.objects.filter(id=currentid).values('hod_name','email')
 
        current_hod = (customuserdata[0]['hod_name'])
 
        hod_email = (customuserdata[0]['email'])
        
        complex_obj = Register.objects.filter(is_active=0,hod_name=current_hod).values('id', 'email', 'password', 'hod_name')
        
        total_user = complex_obj.count()
 
        # Create a list of dictionaries to store user-specific data
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
            print('********************',role1)
            try:
                user_manager = request.POST['user_manager']
            except:
                pass
            if role1 == 'Team Lead':
                id = signing.loads(id)
                user_manager = user_manager
                email1 = Register.objects.get(id=id).email
                username = Register.objects.get(id=id).username
                password1 = Register.objects.get(id=id).password
                hodname = Register.objects.get(id=id).hod_name
 
                try:
                    existing_user_active = Register.objects.get(id=id).is_active
                    if existing_user_active == 1:
                        
                        Register.objects.filter(id=id).update(role=role1,user_manager=user_manager)
                        # Retrieve the user
                        user1 = get_object_or_404(CustomUser, email=email1)
 
                        # Retrieve the group
                        try:
                            group = Group.objects.get(name=role1)
                        except Group.DoesNotExist:
                            # Handle the case where the group doesn't exist
                            return HttpResponse(f"Group '{role1}' does not exist.", status=400)
 
                        # Add the user to the group
                        user1.groups.clear()
                        user1.groups.add(group)
 
                        # Save the changes to the user
                        user1.save()
                        messages.success(request, 'This id user role and AM/Manager updated Successfully.',extra_tags="alert-success")
                        email1 = Register.objects.get(id=id).email
                        username = Register.objects.get(id=id).username
                        print('$$$$$$$$$$',email1,username)
                        CustomUser.objects.filter(email=email1).update(role=role1, user_manager=user_manager)
                        try:
                            TeamLead.objects.create(name=username,email=email1)
                            Manager.objects.filter(name=username,email=email1).delete()
                        except:
                            pass
                        return redirect('/hod_dashboard')
                    else:
                        print('!!!!!!!!!!!')
                        existing_user = Register.objects.filter(id=id).update(is_active=1,role=role1,user_manager=user_manager)
                        user = CustomUser.objects.create_user(email=email1,username=username, password=password1,hod_name=hodname,role=role1,user_manager=user_manager,is_active=1,is_staff=1)
                        
                        user.save()
                        # Retrieve the user
                        user1 = get_object_or_404(CustomUser, email=email1)
 
                        # Retrieve the group
                        try:
                            group = Group.objects.get(name=role1)
                        except Group.DoesNotExist:
                            # Handle the case where the group doesn't exist
                            return HttpResponse(f"Group '{role1}' does not exist.", status=400)
 
                        # Add the user to the group
                        user1.groups.add(group)
 
                        # Save the changes to the user
                        user1.save()
                        messages.success(request, 'Registration Completed',extra_tags="alert-success")
                        return redirect('/hod_dashboard')
                except Register.DoesNotExist:
                    pass
 
            if role1 == 'AM/Manager':
                id = signing.loads(id)
                print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
                email1 = Register.objects.get(id=id).email
                username = Register.objects.get(id=id).username
                password1 = Register.objects.get(id=id).password
                hodname = Register.objects.get(id=id).hod_name
                user_manager = ''
 
                try:
                    existing_user_active = Register.objects.get(id=id).is_active
                    if existing_user_active == 1:
 
                        Register.objects.filter(id=id).update(role=role1,user_manager=user_manager)
                        user1 = get_object_or_404(CustomUser, email=email1)
 
                        # Retrieve the group
                        try:
                            group = Group.objects.get(name=role1)
                        except Group.DoesNotExist:
                            # Handle the case where the group doesn't exist
                            return HttpResponse(f"Group '{role1}' does not exist.", status=400)
 
                        # Add the user to the group
                        user1.groups.clear()
                        user1.groups.add(group)
 
                        # Save the changes to the user
                        user1.save()
                        messages.success(request, 'This id user role and AM/Manager updated Successfully.',extra_tags="alert-success")
                        CustomUser.objects.filter(email=email1).update(role=role1)
                        try:
                            Manager.objects.create(name=username,email=email1)
                            TeamLead.objects.filter(name=username,email=email1).delete()
                        except:
                            pass
                        return redirect('/hod_dashboard')
                    else:
                        
                        existing_user = Register.objects.filter(id=id).update(is_active=1,role=role1,user_manager=user_manager)
                        user = CustomUser.objects.create_user(email=email1,username=username, password=password1,hod_name=hodname,role=role1,user_manager=user_manager,is_active=1,is_staff=1)
                        # CustomUser.objects.filter(email=email1).update(role=role1)
                        user.save()
                        # Retrieve the user
                        user1 = get_object_or_404(CustomUser, email=email1)
 
                        # Retrieve the group
                        try:
                            group = Group.objects.get(name=role1)
                        except Group.DoesNotExist:
                            # Handle the case where the group doesn't exist
                            return HttpResponse(f"Group '{role1}' does not exist.", status=400)
 
                        # Add the user to the group
                        user.groups.clear()
                        user1.groups.add(group)
 
                        # Save the changes to the user
                        user1.save()
                        messages.success(request, 'Registration Completed',extra_tags="alert-success")
                        return redirect('/hod_dashboard')
                except Register.DoesNotExist:
                    pass
                
            if role1 == 'HOD':
                id = signing.loads(id)
                print('?????????????????????')
                email1 = Register.objects.get(id=id).email
                username = Register.objects.get(id=id).username
                password1 = Register.objects.get(id=id).password
                hodname = Register.objects.get(id=id).hod_name
                user_manager = ''
 
                try:
                    existing_user_active = Register.objects.get(id=id).is_active
                    if existing_user_active == 1:
                        
                        Register.objects.filter(id=id).update(role=role1,user_manager=user_manager)
                        # Retrieve the user
                        user1 = get_object_or_404(CustomUser, email=email1)
 
                        # Retrieve the group
                        try:
                            group = Group.objects.get(name=role1)
                        except Group.DoesNotExist:
                            # Handle the case where the group doesn't exist
                            return HttpResponse(f"Group '{role1}' does not exist.", status=400)
 
                        # Add the user to the group
                        user1.groups.clear()
                        user1.groups.add(group)
 
                        # Save the changes to the user
                        user1.save()
                        messages.success(request, 'This id user role and AM/Manager updated Successfully.',extra_tags="alert-success")
                        email1 = Register.objects.get(id=id).email
                        username = Register.objects.get(id=id).username
                        print('$$$$$$$$$$',email1,username)
                        CustomUser.objects.filter(email=email1).update(role=role1)
                        try:
                            Hod.objects.create(name=username,email=email1)
                        except:
                            pass
                        return redirect('/hod_dashboard')
                    else:
                        print('!!!!!!!!!!!')
                        existing_user = Register.objects.filter(id=id).update(is_active=1,role=role1,user_manager=user_manager)
                        user = CustomUser.objects.create_user(email=email1,username=username, password=password1,hod_name=hodname,role=role1,user_manager=user_manager,is_active=1,is_staff=1)
                        
                        user.save()
                        # Retrieve the user
                        user1 = get_object_or_404(CustomUser, email=email1)
 
                        # Retrieve the group
                        try:
                            group = Group.objects.get(name=role1)
                        except Group.DoesNotExist:
                            # Handle the case where the group doesn't exist
                            return HttpResponse(f"Group '{role1}' does not exist.", status=400)
 
                        # Add the user to the group
                        user1.groups.add(group)
 
                        # Save the changes to the user
                        user1.save()
                        messages.success(request, 'Registration Completed',extra_tags="alert-success")
                        return redirect('/hod_dashboard')
                except Register.DoesNotExist:
                    pass
                
         
            email1 = Register.objects.get(id=id).email
            username = Register.objects.get(id=id).username
            password1 = Register.objects.get(id=id).password
            hodname = Register.objects.get(id=id).hod_name
            
            # Check if the email already exists
            try:
                existing_user_active = Register.objects.get(id=id).is_active
                if existing_user_active == 1:
                    Register.objects.filter(id=id).update(role=role1,user_manager=user_manager)
                    # Retrieve the user
                    user1 = get_object_or_404(CustomUser, email=email1)
 
                    # Retrieve the group
                    try:
                        group = Group.objects.get(name=role1)
                    except Group.DoesNotExist:
                        # Handle the case where the group doesn't exist
                        return HttpResponse(f"Group '{role1}' does not exist.", status=400)
 
                    # Add the user to the group
                    user1.groups.clear()
                    user1.groups.add(group)
 
                    # Save the changes to the user
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
 
            # Create a new user
            try:
                
                existing_user = Register.objects.filter(id=id).update(is_active=1,role=role1,user_manager=user_manager)
                user = CustomUser.objects.create_user(email=email1,username=username,password=password1,hod_name=hodname,role=role1,user_manager=user_manager,is_active=1,is_staff=1)
                user.save()
                # Retrieve the user
                user1 = get_object_or_404(CustomUser, email=email1)
 
                # Retrieve the group
                try:
                    group = Group.objects.get(name=role1)
                except Group.DoesNotExist:
                    # Handle the case where the group doesn't exist
                    return HttpResponse(f"Group '{role1}' does not exist.", status=400)
 
                # Add the user to the group
                user1.groups.add(group)
 
                # Save the changes to the user
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
    # If user is already authenticated, redirect them to their dashboard
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')

    # Continue with the regular login logic if not authenticated
    if request.method == 'POST':
        email = request.POST.get('email')
        user_password = request.POST.get('login_password')

        # Authenticate the user
        user = authenticate(request, email=email, password=user_password)

        if user is not None:
            request.session['currentuser_id'] = user.id
            login(request, user)

            # Redirect to the dashboard if already authenticated
            next_url = request.GET.get('next', None)
            if next_url and not next_url.startswith('/login'):
                return redirect(next_url)

            return redirect('dashboard_redirect') 

        else:
            messages.error(request, 'Invalid login credentials.', extra_tags="alert-danger")

    return render(request, 'novusapp/login.html')


@login_required
def dashboard_redirect(request):
    # If user is already authenticated, redirect to their dashboard
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

    # If not authenticated, handle as before
    return redirect('/')


@login_required
@role_required(allowed_roles=['Team Lead'])
def user_dashboard(request):
    if request.session.has_key('currentuser_id'):
        userid = request.session['currentuser_id']
        print('userid',userid)
        TeamLeadname = CustomUser.objects.get(id=userid).username
        TeamLead_email = CustomUser.objects.get(id=userid).email
        user_manager = CustomUser.objects.get(id=userid).user_manager

        try:
            department_obj=get_object_or_404(CustomUser, id=int(userid))
        
        except:
            department_obj=""

        try:
            hod_name = CustomUser.objects.get(id=userid).hod_name
            print(hod_name)
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

        industry = Industry.objects.filter(is_active=True).all() 
        mycountry = Country.objects.filter(is_active=True).all()
        if request.method == 'POST':
            try:
                # Get the data from the POST request
                respondent_name = request.POST.get('respondent_name')
                job_title = request.POST.get('job_title')
                country_name = request.POST.get('country')
                industry_name = request.POST.get('industry')
                company_name = request.POST.get('company')
                profile_link = request.POST.get('profile_link')
                meeting_link = request.POST.get('meeting_link')
                analyst_name = request.POST.get('analyst')
                project_name = request.POST.get('project')
                project_type = request.POST.get('project_type')
                company_revenue = request.POST.get('company_revenue')
                company_strength = request.POST.get('company_strength')
                incentive_name = request.POST.get('incentive')
                interview_duration = request.POST.get('interview_duration')
                interview_date = request.POST.get('interview_date')

                
                # Create or retrieve related records from other tables
                try:
                    job = Job.objects.get(title=job_title)
                except Job.DoesNotExist:
                    job = Job.objects.create(title=job_title)
                # Use filter instead of get for cases where there might be multiple matches
                countries = Country.objects.filter(name=country_name)
                if countries.exists():
                    country = countries.first()
                else:
                    country = Country.objects.create(name=country_name)

                industries = Industry.objects.filter(name=industry_name)
                if industries.exists():
                    industry = industries.first()
                else:
                    industry = Industry.objects.create(name=industry_name)

                companies = Company.objects.filter(name=company_name, revenue=company_revenue, strength=company_strength)
                if companies.exists():
                    company = companies.first()
                else:
                    company = Company.objects.create(name=company_name, revenue=company_revenue, strength=company_strength)

                analysts = Analyst.objects.filter(title=analyst_name)
                if analysts.exists():
                    analyst = analysts.first()
                else:
                    analyst = Analyst.objects.create(title=analyst_name)

                # Retrieve or create the project
                projects = Project.objects.filter(name=project_name, project_type=project_type)
                if projects.exists():
                    project = projects.first()
                else:
                    project = Project.objects.create(name=project_name, project_type=project_type)

                # Retrieve or create the project interview using the project
                project_interviews = ProjectInterview.objects.filter(project=project)
                if project_interviews.exists():
                    project_interview = project_interviews.first()
                else:
                    project_interview = ProjectInterview.objects.create(
                        project=project,
                        interview_duration=interview_duration,
                        interview_date=interview_date
                    )

                # Retrieve or create the incentive using the project
                incentives = Incentive.objects.filter(project=project)
                if incentives.exists():
                    incentive = incentives.first()
                else:
                    incentive = Incentive.objects.create(project=project, Unique_identifier=incentive_name)




                # Create the Respondent instance and associate it with the related records
                respondent = Respondent.objects.create(
                    name=respondent_name,
                    job=job,
                    email=TeamLead_email,
                    user_manager=user_manager,
                    hod_email=hod_email,
                    user_manager_email = user_manager_email,
                    country=country,
                    industry=industry,
                    company=company,
                    profile_link=profile_link,
                    meeting_link=meeting_link,
                    analyst=analyst,
                    project=project,
                    incentive=incentive,
                    project_interview=project_interview,
                    team_lead = TeamLeadname,
                    Department=department_obj.dep.name,
                    is_active = 0
                )

                # Save the Respondent instance to the database
                respondent.save()
                messages.success(request, 'Form Submitted Successfully',extra_tags="alert-success")
                return redirect('/user_dashboard')

            except Exception as e:
                messages.error(request, f'Error: {e}', extra_tags="alert-danger")
                return redirect('/user_dashboard')
        

        context = {
            'industry':industry,
            'allcountry':mycountry
            }
        return render(request,"novusapp/user_dashboard.html",context)
    
    return HttpResponse('Please login')


@login_required
@role_required(allowed_roles=['Team Lead'])
def userdata(request):
    if request.session.has_key('currentuser_id'):
        # Retrieve all data from the Respondent table
        userid = request.session['currentuser_id']
        name = CustomUser.objects.get(id=userid).username
        useremail = CustomUser.objects.get(id=userid).email
        dep = CustomUser.objects.get(id=userid).department

        # Retrieve the 'type' parameter from the GET request
        data_type = request.GET.get('type')

        # Get items per page from the request, default to 10 if not specified
        items_per_page = int(request.GET.get('items_per_page', 10))

        # Filter data based on 'type' parameter
        if data_type == 'self':
            respondents = Respondent.objects.filter(email=useremail, is_active__in=[0,1]).all()
        elif data_type == 'all':
            respondents = Respondent.objects.filter(Q(email=useremail, is_active=1) | Q(is_active=1)).all()
        else:
            respondents = Respondent.objects.filter(email=useremail, is_active__in=[0,1]).all()

        # Paginator
        paginator = Paginator(respondents, items_per_page)
        page_number = request.GET.get('page')

        try:
            servicedatafinal = paginator.page(page_number)
        except PageNotAnInteger:
            servicedatafinal = paginator.page(1)
        except EmptyPage:
            servicedatafinal = paginator.page(paginator.num_pages)

        # Get total page count for pagination links
        totalpage = servicedatafinal.paginator.num_pages
        totalpagelist = [i + 1 for i in range(totalpage)]

        # Create the URL for pagination links
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
@role_required(allowed_roles=['HOD'])
def userhod_data(request):
    if request.session.has_key('currentuser_id'):

        userid = request.session['currentuser_id']
        name = CustomUser.objects.get(id=userid).username
        hodname = CustomUser.objects.get(id=userid).hod_name
        hodemail = CustomUser.objects.get(id=userid).email
       
        # Retrieve the 'type' parameter from the GET request
        data_type = request.GET.get('type')
        
        # Get items per page from the request, default to 10 if not specified
        items_per_page = int(request.GET.get('items_per_page', 10))

        # Filter data based on 'type' parameter
        if data_type == 'self':
            respondents = Respondent.objects.filter(hod_email=hodemail, is_active__in=[0,1]).all()
        elif data_type == 'all':
            respondents = Respondent.objects.filter(Q(hod_email=hodemail, is_active=1) | Q(is_active=1)).all()
        else:
            # Handle other cases if needed
            respondents = Respondent.objects.filter(hod_email=hodemail, is_active__in=[0,1]).all()

        # Paginator
        paginator = Paginator(respondents, items_per_page)
        page_number = request.GET.get('page')

        try:
            servicedatafinal = paginator.page(page_number)
        except PageNotAnInteger:
            servicedatafinal = paginator.page(1)
        except EmptyPage:
            servicedatafinal = paginator.page(paginator.num_pages)

        # Get total page count for pagination links
        totalpage = servicedatafinal.paginator.num_pages
        totalpagelist = [i + 1 for i in range(totalpage)]

        # Create the URL for pagination links
        base_url = reverse('userhod_data')
        pagination_url = f"{base_url}?type={data_type}&items_per_page={items_per_page}&page="

        context = {
            'respondents': servicedatafinal,
            'name': name,
            'lastpage': totalpage,
            'totalpagelist': totalpagelist,
            'items_per_page': items_per_page,
            'pagination_url': pagination_url,  # Pass the pagination URL to the template
        }

        return render(request, "novusapp/userhod_data.html", context)

    return HttpResponse('Please Login')



def autocomplete(request):
    if 'term' in request.GET:
        terms = request.GET.get('term').split(',')
        term = terms[-1].strip()  # Get the last term after the last comma

        qs = Industry.objects.filter(is_active=True,name__icontains=term)
        titles = [product.name for product in qs]
        print('@@@@@@@@@@@@@@@@@/',titles)

        return JsonResponse(titles, safe=False)
    
    return render(request, 'novusapp/userhod_data.html')


def autocomplete1(request):
    if 'term' in request.GET:
        terms = request.GET.get('term').split(',')
        term = terms[-1].strip()  # Get the last term after the last comma

        qs = Country.objects.filter(is_active=True,name__icontains=term)
        titles = [product.name for product in qs]

        return JsonResponse(titles, safe=False)
    
    return render(request, 'novusapp/userhod_data.html')


def autocomplete2(request):
    if 'term' in request.GET:
        terms = request.GET.get('term').split(',')
        term = terms[-1].strip()  # Get the last term after the last comma

        qs = Job.objects.filter(is_active=True,title__icontains=term)
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

        # Create a list of dictionaries to store user-specific data
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
            # 'host_url' : host_url,
        }
        
        return render(request, "novusapp/tables.html", context)

    return HttpResponse('Please login')


def logout_view(request):
    # Clear the user's session
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

        # Create a list of dictionaries to store user-specific data
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

        # Retrieve the 'type' parameter from the GET request
        data_type = request.GET.get('type')

        # Get items per page from the request, default to 10 if not specified
        items_per_page = int(request.GET.get('items_per_page', 10))

        # Filter data based on 'type' parameter
        if data_type == 'self':
            respondents = Respondent.objects.filter(user_manager_email=current_manager_email, is_active__in=[0, 1]).all()
        elif data_type == 'all':
            respondents = Respondent.objects.filter(Q(user_manager_email=current_manager_email, is_active=1) | Q(is_active=1)).all()
        else:
            # Handle other cases if needed
            respondents = Respondent.objects.filter(user_manager_email=current_manager_email, is_active__in=[0, 1]).all()

        # Paginator
        paginator = Paginator(respondents, items_per_page)
        page_number = request.GET.get('page')

        try:
            servicedatafinal = paginator.page(page_number)
        except PageNotAnInteger:
            servicedatafinal = paginator.page(1)
        except EmptyPage:
            servicedatafinal = paginator.page(paginator.num_pages)

        # Get total page count for pagination links
        totalpage = servicedatafinal.paginator.num_pages
        totalpagelist = [i + 1 for i in range(totalpage)]

        # Create the URL for pagination links
        base_url = reverse('manager')
        pagination_url = f"{base_url}?type={data_type}&items_per_page={items_per_page}&page="

        context = {
            'respondents': servicedatafinal,
            'name': name,
            'lastpage': totalpage,
            'totalpagelist': totalpagelist,
            'hod': current_manager,
            'items_per_page': items_per_page,
            'pagination_url': pagination_url,  # Pass the pagination URL to the template
        }

        return render(request, "novusapp/teamlead_data.html", context)

    return HttpResponse('Please Login')


@login_required
@role_required(allowed_roles=['AM/Manager'])
def managerteam_data(request):
    if request.session.has_key('currentuser_id'):
        # Retrieve all data from the Respondent table
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
        dep = Department.objects.filter(is_active=True).all()

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
                    
                
                #Update user information
                if CustomUser.objects.filter(dep=dept, mobile=mobile).exists():
                    messages.info(request, 'Same record already exists.', extra_tags="alert-warning")
                    return redirect('/profile')
                
                CustomUser.objects.filter(id=id).update(dep=dept, mobile=mobile)
                
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
        # Handle other exceptions
        messages.error(request, f'An error occurred: {str(e)}', extra_tags="alert-danger")
        return render(request, "novusapp/edit.html", {'department': dep})



def change_password(request):
    # Get the user ID from the session
    userid = request.session.get('currentuser_id')
    role = CustomUser.objects.get(id=userid).role
    name = CustomUser.objects.get(id=userid).username
    if request.method == 'POST':
        # Get the old, new, and confirmed passwords from the form
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        # confirm_password = request.POST.get('confirm_password')
        
       
        # Retrieve the user object from the database
        user = CustomUser.objects.get(id=userid)

        # Check if the old password matches the user's current password
        if not check_password(old_password, user.password):
            messages.error(request, 'Old password is incorrect',extra_tags="alert-danger")
            return redirect('/profile/change_password')  # Adjust the URL name to your view

        if old_password == new_password:
            messages.warning(request,"Old and new password same please change this password.", extra_tags="alert-warning")
            return redirect("/profile/change_password")


        user.set_password(new_password)
        user.save()

        messages.success(request, 'Password changed successfully',extra_tags="alert-success")
        return redirect('/')  # Redirect to the profile page or another appropriate page

    context = {
        'role':role,
        'username':name}
    return render(request, 'novusapp/change_password.html',context)  





# login templates render

def loginDemo(request):
    return render(request, 'novusapp/base1.html')


def logout_view(request):
    logout(request)
    return redirect('/')











