from .models import CustomUser,Register
from django.shortcuts import get_object_or_404

def add_username_to_context(request):
    username = ""
    Role=""
    total_user = ""
    id = ""
    # Check if 'currentuser_id' is in the session
    if 'currentuser_id' in request.session:
        userid = request.session['currentuser_id']
        try:
            username = get_object_or_404(CustomUser,id=userid).username
            Role = get_object_or_404(CustomUser,id=userid).role
            customuserdata = CustomUser.objects.filter(id=userid).values('hod_name','email')
            
            current_hod = (customuserdata[0]['hod_name'])
            hod_email = (customuserdata[0]['email'])
            complex_obj = Register.objects.filter(is_active=0,hod_name=current_hod).values('id', 'email', 'password', 'hod_name')
            total_user = complex_obj.count()
            id = userid
        except CustomUser.DoesNotExist:
            pass  # Handle the case where the user does not exist
    context = {
        'username' : username,
        'Role' : Role,
        "total_user" : total_user,
        "id": id
    }
    return context
