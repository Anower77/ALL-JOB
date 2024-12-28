from django.contrib import admin
from .models import JobListing, JobApplication, CustomUser

# Register your models here
admin.site.register(JobListing)
admin.site.register(JobApplication)
admin.site.register(CustomUser)
