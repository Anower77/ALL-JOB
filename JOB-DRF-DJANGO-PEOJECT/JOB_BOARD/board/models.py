from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings



# Create your models here.
# class CustomUser(AbstractUser):
#     ROLE_CHOICES = [
#         ('employer', 'Employer'),
#         ('job_seeker', 'Job Seeker'),
#     ]
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES)


# Job Listing
class JobListing(models.Model):
    # Existing fields
    CATEGORY_CHOICES = [
        ('IT', 'Information Technology'),
        ('HR', 'Human Resources'),
        ('FIN', 'Finance'),
        ('MKT', 'Marketing'),
        ('EDU', 'Education'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=100)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_listings')
    date_posted = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='IT')  # Added category

    def __str__(self):
        return self.title




# Job Application
class JobApplication(models.Model):
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True, null=True)
    date_applied = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.username} applied for {self.job.title}"


