# middleware.py
from django.utils.deprecation import MiddlewareMixin
from novusapp.models import CustomUser
from django.contrib import messages

from django.shortcuts import redirect
from django.contrib import messages

class IsActiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if the user is authenticated and not active
        if request.user.is_authenticated and not request.user.is_active:
            print(request.user)
            
            # Redirect to the login page with a message
            messages.error(request, "Your account is not active. Please contact support.")
            return redirect('login')  # Replace 'login' with the actual name or URL of your login page

        return response