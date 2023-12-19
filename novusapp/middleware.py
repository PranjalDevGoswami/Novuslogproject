# middleware.py
from django.utils.deprecation import MiddlewareMixin

class RoleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Your logic to assign roles based on user attributes
        # Example: request.user.roles.add(Role.objects.get(name='Admin'))
        pass
