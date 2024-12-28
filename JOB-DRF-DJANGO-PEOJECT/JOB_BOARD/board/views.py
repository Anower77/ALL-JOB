from django.shortcuts import render, redirect

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer, JobApplicationSerializer

from rest_framework import generics, permissions
from .models import JobListing
from .serializers import JobListingSerializer

from .models import JobApplication

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from django.contrib.auth.decorators import login_required
from .utils import send_email

from django.contrib.auth.views import LoginView
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class CustomLoginView(LoginView):
    template_name = 'board/login.html'  



class UserRegistrationView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]



# Login View
def loginView(request):
    return render(request, 'board/login.html')

# Logout View
def logoutView(request):
    return render(request, 'board/logout.html')

# Employer Dashboard View
def employer_dashboard(request):
    # Add any context data required for the template
    return render(request, 'board/employer_dashboard.html')

# Job Seeker Dashboard View
def job_seeker_dashboard(request):
    # Add any context data required for the template
    return render(request, 'board/job_seeker_dashboard.html')

# employer dashboard
@login_required
def employer_dashboard(request):
    return render(request, 'board/employer_dashboard.html')





# Create your views here.
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Job Listing List Create View
class JobListingListCreateView(generics.ListCreateAPIView):
    queryset = JobListing.objects.all().order_by('-date_posted')
    serializer_class = JobListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)


# Job Listing Detail View
class JobListingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobListing.objects.all()
    serializer_class = JobListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



# Job Application List CreateView
class JobApplicationListCreateView(generics.ListCreateAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JobApplication.objects.filter(job__id=self.kwargs['job_id'])

    def perform_create(self, serializer):
        serializer.save(
            applicant=self.request.user,
            job_id=self.kwargs['job_id']
        )





# Employer Dashboard View
class EmployerDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not request.user.is_employer:  # Assuming `is_employer` is a field on the User model
            return Response({"error": "Access denied"}, status=403)

        job_listings = JobListing.objects.filter(posted_by=request.user)
        data = []
        for job in job_listings:
            applications = job.applications.all()
            job_data = {
                "job_title": job.title,
                "applications": JobApplicationSerializer(applications, many=True).data,
            }
            data.append(job_data)
        return Response(data)




# Job Seeker Dashboard View
class JobSeekerDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.is_employer:  # Assuming `is_employer` is a field on the User model
            return Response({"error": "Access denied"}, status=403)

        applications = JobApplication.objects.filter(applicant=request.user)
        return Response(JobApplicationSerializer(applications, many=True).data)




# Job Listing ViewSet
class JobListingViewSet(viewsets.ModelViewSet):
    queryset = JobListing.objects.all()
    serializer_class = JobListingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category']  # Enable category filtering



# Job Application List CreateView
class JobApplicationListCreateView(generics.ListCreateAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JobApplication.objects.filter(job__id=self.kwargs['job_id'])

    def perform_create(self, serializer):
        application = serializer.save(
            applicant=self.request.user,
            job_id=self.kwargs['job_id']
        )
        # Send email to employer
        employer_email = application.job.posted_by.email
        send_email(
            subject="New Job Application",
            message=f"You have received a new application for your job '{application.job.title}'.",
            recipient_list=[employer_email],
        )
        # Send email to applicant
        send_email(
            subject="Application Submitted",
            message=f"Your application for the job '{application.job.title}' has been successfully submitted.",
            recipient_list=[self.request.user.email],
        )





# Job Application Detail View
class JobApplicationDetailView(APIView):
    def get(self, request, job_id, pk):
        try:
            application = JobApplication.objects.get(id=pk, job_id=job_id)
            serializer = JobApplicationSerializer(application)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except JobApplication.DoesNotExist:
            return Response({"error": "Job Application not found"}, status=status.HTTP_404_NOT_FOUND)
