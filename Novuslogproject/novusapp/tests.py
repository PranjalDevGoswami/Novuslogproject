from django.test import TestCase

# Create your tests here.


from django.test import TestCase
from django.utils import timezone
from .models import Job, Country, Industry, Company, Analyst, Department, Project, Incentive, ProjectInterview, Respondent, RoleMaster, Hod, TeamLead, Manager, Register, CustomUser


class ModelTestCase(TestCase):
    def setUp(self):
        # Create sample data for testing
        self.job = Job.objects.create(title="Test Job", is_active=True)
        self.country = Country.objects.create(name="Test Country", is_active=True)
        self.industry = Industry.objects.create(name="Test Industry", is_active=True)
        self.company = Company.objects.create(name="Test Company", revenue="1000", strength="50", is_active=True)
        self.analyst = Analyst.objects.create(title="Test Analyst", is_active=True)
        self.department = Department.objects.create(name="Test Department", is_active=True)
        self.project = Project.objects.create(name="Test Project", project_type="TypeA", project_code="ABC123", LOI="123", is_active=True)
        self.incentive = Incentive.objects.create(project=self.project, Unique_identifier="12345", is_active=True)
        self.project_interview = ProjectInterview.objects.create(project=self.project, interview_duration="1 hour", interview_date="2023-01-01", is_active=True)
        self.respondent = Respondent.objects.create(
            name="Test Respondent", job=self.job, email="test@example.com", user_manager="ManagerA",
            user_manager_email="manager@example.com", hod_email="hod@example.com", country=self.country,
            industry=self.industry, company=self.company, profile_link="http://user1profile1.com/profile",
            meeting_link="http://novusinsights.com/meeting", analyst=self.analyst, project=self.project,
            incentive=self.incentive, project_interview=self.project_interview, team_lead="LeadA", Department="Test Department",
            is_active=True
        )
        self.role = RoleMaster.objects.create(name="Test Role", is_active=True)
        self.hod = Hod.objects.create(name="Test HOD", email="hod@example.com", is_active=True)
        self.team_lead = TeamLead.objects.create(name="Test Team Lead", email="lead@example.com", is_active=True)
        self.manager = Manager.objects.create(name="Test Manager", email="manager@example.com", is_active=True)
        self.register = Register.objects.create(email="register@example.com", username="testuser", password="securepassword", hod_name="Test HOD", is_active=True)
        self.custom_user = CustomUser.objects.create(email="customuser@example.com", username="customuser", role="Test Role", user_manager="ManagerA", hod_name="Test HOD", department="Test Department", mobile="123456789", token="token123", otp="123456", is_superviser="Yes", is_category="A", is_active=True)

    def test_job_model(self):
        self.assertEqual(str(self.job), "Test Job")

    def test_country_model(self):
        self.assertEqual(str(self.country), "Test Country")

    # Add similar test methods for other models...

    def test_custom_user_model(self):
        self.assertEqual(str(self.custom_user), "customuser@example.com")