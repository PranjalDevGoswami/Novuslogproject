from .models import Country
from faker import Faker
fake = Faker()


def seed_db(n):
    for i in range(0,n):
        Country.objects.create(name=fake.country())
        
        
               