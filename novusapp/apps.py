from django.apps import AppConfig


class NovusappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'novusapp'
    
    def ready(self):
        import novusapp.signals  # Import signals module
    

    


   
